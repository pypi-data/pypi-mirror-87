/***
 *    Description:  Stream table data.
 *
 *         Author:  Dilawar Singh <dilawars@ncbs.res.in>
 *   Organization:  NCBS Bangalore
 */

#include <algorithm>
#include <sstream>

#include "../basecode/global.h"
#include "../basecode/header.h"
#include "Streamer.h"
#include "../scheduling/Clock.h"
#include "../utility/utility.h"
#include "../shell/Shell.h"


const Cinfo* Streamer::initCinfo()
{
    /*-----------------------------------------------------------------------------
     * Finfos
     *-----------------------------------------------------------------------------*/
    static ValueFinfo< Streamer, string > datafile(
        "datafile"
        , "File/stream to write table data to. Default is is __moose_tables__.dat.n"
        " By default, this object writes data every second \n"
        , &Streamer::setDatafilePath
        , &Streamer::getDatafilePath
    );

    static ValueFinfo< Streamer, string > outfile(
        "outfile"
        , "Use datafile (deprecated)"
        , &Streamer::setDatafilePath
        , &Streamer::getDatafilePath
    );


    static ValueFinfo< Streamer, string > format(
        "format"
        , "Format of output file, default is csv"
        , &Streamer::setFormat
        , &Streamer::getFormat
    );

    static ReadOnlyValueFinfo<Streamer, unsigned int> numTables (
        "numTables"
        , "Number of Tables handled by Streamer "
        , &Streamer::getNumTables
    );

    static ReadOnlyValueFinfo<Streamer, unsigned int> numWriteEvents(
        "numWriteEvents"
        , "Number of time streamer was called to write. (For debugging/performance reason only)"
        , &Streamer::getNumWriteEvents
    );

    /*-----------------------------------------------------------------------------
     *
     *-----------------------------------------------------------------------------*/
    static DestFinfo process(
        "process"
        , "Handle process call"
        , new ProcOpFunc< Streamer >( &Streamer::process )
    );

    static DestFinfo reinit(
        "reinit"
        , "Handles reinit call"
        , new ProcOpFunc< Streamer > ( &Streamer::reinit )
    );


    static DestFinfo addTable(
        "addTable"
        , "Add a table to Streamer"
        , new OpFunc1<Streamer, ObjId>( &Streamer::addTable )
    );

    static DestFinfo addTables(
        "addTables"
        , "Add many tables to Streamer"
        , new OpFunc1<Streamer, vector<ObjId> >( &Streamer::addTables )
    );

    static DestFinfo removeTable(
        "removeTable"
        , "Remove a table from Streamer"
        , new OpFunc1<Streamer, ObjId>( &Streamer::removeTable )
    );

    static DestFinfo removeTables(
        "removeTables"
        , "Remove tables -- if found -- from Streamer"
        , new OpFunc1<Streamer, vector<ObjId> >( &Streamer::removeTables )
    );

    /*-----------------------------------------------------------------------------
     *  ShareMsg definitions.
     *-----------------------------------------------------------------------------*/
    static Finfo* procShared[] =
    {
        &process, &reinit, &addTable, &addTables, &removeTable, &removeTables
    };

    static SharedFinfo proc(
        "proc",
        "Shared message for process and reinit",
        procShared, sizeof( procShared ) / sizeof( const Finfo* )
    );

    static Finfo * tableStreamFinfos[] =
    {
        &datafile, &outfile, &format, &proc, &numTables, &numWriteEvents
    };

    static string doc[] =
    {
        "Name", "Streamer",
        "Author", "Dilawar Singh, 2016, NCBS, Bangalore.",
        "Description", "Streamer: Stream moose.Table data to out-streams\n"
    };

    static Dinfo< Streamer > dinfo;

    static Cinfo tableStreamCinfo(
        "Streamer",
        TableBase::initCinfo(),
        tableStreamFinfos,
        sizeof( tableStreamFinfos )/sizeof(Finfo *),
        &dinfo,
        doc,
        sizeof(doc) / sizeof(string)
    );

    return &tableStreamCinfo;
}

static const Cinfo* tableStreamCinfo = Streamer::initCinfo();

// Class function definitions

Streamer::Streamer()
{
    // Not all compilers allow initialization during the declaration of class
    // methods.
    format_ = "csv";
    numWriteEvents_ = 0;
    columns_.push_back("time");               /* First column is time. */
    tables_.resize(0);
    tableIds_.resize(0);
    tableTick_.resize(0);
    tableDt_.resize(0);
    data_.resize(0);
}

Streamer& Streamer::operator=( const Streamer& st )
{
    return *this;
}


Streamer::~Streamer()
{
}

/**
 * @brief Reinit.
 *
 * @param e
 * @param p
 */
void Streamer::reinit(const Eref& e, ProcPtr p)
{

    if( tables_.size() == 0 )
    {
        moose::showWarn( "Zero tables in streamer. Disabling Streamer" );
        e.element()->setTick( -2 );             /* Disable process */
        return;
    }

    Clock* clk = reinterpret_cast<Clock*>( Id(1).eref().data() );
    for (unsigned int i = 0; i < tableIds_.size(); i++)
    {
        int tickNum = tableIds_[i].element()->getTick();
        double tick = clk->getTickDt( tickNum );
        tableDt_.push_back( tick );
        // Make sure that all tables have the same tick.
        if( i > 0 )
        {
            if( tick != tableDt_[0] )
            {
                moose::showWarn( "Table " + tableIds_[i].path() + " has "
                                 " different clock dt. "
                                 " Make sure all tables added to Streamer have the same "
                                 " dt value."
                               );
            }
        }
    }


    // Push each table dt_ into vector of dt
    for( unsigned int i = 0; i < tables_.size(); i++)
    {
        Id tId = tableIds_[i];
        int tickNum = tId.element()->getTick();
        tableDt_.push_back( clk->getTickDt(tickNum) );
    }

    // Make sure all tables have same dt_ else disable the streamer.
    vector<unsigned int> invalidTables;
    for (unsigned int i = 1; i < tableTick_.size(); i++)
    {
        if( tableTick_[i] != tableTick_[0] )
        {
            LOG( moose::warning
                 , "Table " << tableIds_[i].path()
                 << " has tick (dt) which is different than the first table."
                 << endl
                 << " Got " << tableTick_[i] << " expected " << tableTick_[0]
                 << endl << " Disabling this table."
               );
            invalidTables.push_back( i );
        }
    }

    for (unsigned int i = 0; i < invalidTables.size(); i++)
    {
        tables_.erase( tables_.begin() + i );
        tableDt_.erase( tableDt_.begin() + i );
        tableIds_.erase( tableIds_.begin() + i );
    }

    if( ! isOutfilePathSet_ )
    {
        string defaultPath = "_tables/" + moose::moosePathToUserPath( e.id().path() );
        setDatafilePath( defaultPath );
    }

    // Prepare data. Add columns names and write whatever values are available
    // write now.
    currTime_ = 0.0;
    zipWithTime( );
    StreamerBase::writeToOutFile(datafilePath_, format_, WRITE, data_, columns_);
    data_.clear( );
}

/**
 * @brief This function is called from Shell when simulation is called to write
 * the left-over data to streamer file.
 */
void Streamer::cleanUp( )
{
    zipWithTime( );
    StreamerBase::writeToOutFile( datafilePath_, format_, APPEND, data_, columns_ );
    data_.clear( );
}

/**
 * @brief This function is called at its clock tick.
 *
 * @param e
 * @param p
 */
void Streamer::process(const Eref& e, ProcPtr p)
{
    // LOG( moose::debug, "Writing Streamer data to file." );
    zipWithTime( );
    StreamerBase::writeToOutFile( datafilePath_, format_, APPEND, data_, columns_ );
    data_.clear();
    numWriteEvents_ += 1;
}


/**
 * @brief Add a table to streamer.
 *
 * @param table Id of table.
 */
void Streamer::addTable( ObjId table )
{
    // If this table is not already in the vector, add it.
    for( unsigned int i = 0; i < tableIds_.size(); i++)
        if( table.path() == tableIds_[i].path() )
            return;                             /* Already added. */

    Table* t = reinterpret_cast<Table*>(table.eref().data());
    tableIds_.push_back( table );
    tables_.push_back( t );
    tableTick_.push_back( table.element()->getTick() );

    // NOTE: Table can also have name. If name is set by User, use the name to
    // for column name, else use modify the table path to generate a suitable
    // column name.
    if(t->getColumnName().size() > 0)
        columns_.push_back(t->getColumnName());
    else
        columns_.push_back(moose::moosePathToColumnName(table.path()));
}

/**
 * @brief Add multiple tables to Streamer.
 *
 * @param tables
 */
void Streamer::addTables( vector<ObjId> tables )
{
    if( tables.size() == 0 )
        return;
    for(auto it = tables.begin(); it != tables.end(); it++)
        addTable( *it );
}


/**
 * @brief Remove a table from Streamer.
 *
 * @param table. Id of table.
 */
void Streamer::removeTable( ObjId table )
{
    int matchIndex = -1;
    for (unsigned int i = 0; i < tableIds_.size(); i++)
        if( table.path() == tableIds_[i].path() )
        {
            matchIndex = i;
            break;
        }

    if( matchIndex > -1 )
    {
        tableIds_.erase( tableIds_.begin() + matchIndex );
        tables_.erase( tables_.begin() + matchIndex );
        columns_.erase( columns_.begin() + matchIndex );
    }
}

/**
 * @brief Remove multiple tables -- if found -- from Streamer.
 *
 * @param tables
 */
void Streamer::removeTables( vector<ObjId> tables )
{
    for(auto it = tables.cbegin(); it != tables.cend(); it++)
        removeTable( *it );
}

/**
 * @brief Get the number of tables handled by Streamer.
 *
 * @return  Number of tables.
 */
unsigned int Streamer::getNumTables( void ) const
{
    return tables_.size();
}

/* --------------------------------------------------------------------------*/
/**
 * @Synopsis  Get number of write events in streamer. Useful for debugging and
 * performance measuerments.
 *
 * @Returns
 */
/* ----------------------------------------------------------------------------*/
unsigned int Streamer::getNumWriteEvents( void ) const
{
    return numWriteEvents_;
}


string Streamer::getDatafilePath( void ) const
{
    return datafilePath_;
}

void Streamer::setDatafilePath( string filepath )
{
    datafilePath_ = filepath;
    isOutfilePathSet_ = true;
    if( ! moose::createParentDirs( filepath ) )
        datafilePath_ = moose::toFilename( datafilePath_ );

    string format = moose::getExtension( datafilePath_, true );
    if( format.size() > 0)
        setFormat( format );
    else
        setFormat( "csv" );
}

/* Set the format of all Tables */
void Streamer::setFormat( string fmt )
{
    format_ = fmt;
}

/*  Get the format of all tables. */
string Streamer::getFormat( void ) const
{
    return format_;
}

/**
 * @brief This function prepares data to be written to a file.
 */
void Streamer::zipWithTime( )
{
    unsigned int numEntriesInEachTable = tables_[0]->getVecSize( );

    //LOG( moose::debug, "Entries in each table " << numEntriesInEachTable );

    // Collect data from all table. If some table does not have enough data,
    // fill it with nan
    vector< vector< double > > collectedData;
    for( unsigned int i = 0; i < tables_.size( ); i++ )
    {
        vector<double> tVec( tables_[i]->getVector( ) );
        if( tVec.size( ) <= numEntriesInEachTable )
        {
#if 0
            LOG( moose::debug
                 , "Table " << tables_[i]->getName( ) << " is not functional. Filling with zero "
               );
#endif
            tVec.resize( numEntriesInEachTable, 0 );
        }
        collectedData.push_back( tVec );
    }

    // Turn it into a table format. Its like taking a transpose of vector<
    // vector >.
    double allTableDt = tableDt_[ 0 ];
    for( unsigned int i = 0; i < collectedData[0].size( ); i++ )
    {
        data_.push_back( currTime_ );
        currTime_ += allTableDt;
        for( unsigned int ii = 0; ii < collectedData.size(); ii++ )
            data_.push_back( collectedData[ ii ][ i ] );
    }

    // After collection data from table, clear tables.
    for(unsigned int i = 0; i < tables_.size(); i++ )
        tables_[i]->clearVec( );

    return;
}
