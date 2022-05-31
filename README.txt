Design:
    Market data can be requested from MktData class. This class will contain
    instances of all supported exchanges. It creates them using a factory(MDFactory).
    The aim is to provide this data in a normalised form to clients of this class.
    Normalised form can be a pandas dataframe perhaps.
    Currently using zerorpc for communication across services, but ideally we
    should have a wrapper around so that we can change the underlying middleware
    without having to change application code.

Build:
    From root folder(altonomy_test):
    docker compose build

Run:
    From root folder(altonomy_test):
    docker compose up


Current State:
    Embarassing - Not much progress has been made - just able to create the docker compose
    application which currently only contains the mkt data(not fully implemented either)
    and mysql part which is only a zerorpc client and dows not even have mysql

    The whole thing was a new concept for me starting from docker! Even python I have
    not used to the level as the main application(used it only as side application).
    This is causing me to take more time.
