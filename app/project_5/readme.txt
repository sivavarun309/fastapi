Alembic
- lightweight database migration tool for when using SQLAlchemy
- Migration tools allow to plan, transfer and upgrade resources within database
- Alembic allows you to change a SQLAlchemy database table after it has been created
- current SQLAlchemy will only create new database tables for us, but not enhance any like add columns or alter
- alembic is a powerful migration tool that allows us to modify our database schemes
- as our application evolves, our database will need to evolve as well
- alembic helps us be able to keep modifying our database to keep up with rapid development requirements

    we will be using alembic on tables that already have data. this allows us to be able to continually create additional content
that works within our application

Alembic Commands and details
- alembic init <folder name>    :    Initializes a new, generic environment
- alembic revision -m <message> :    creates a new revision of the environment
- alembic upgrade <revision #>  :    to create a unique id, used to run our upgrade migration to our database
- alembic downgrade -1          :    Run our downgrade migration to our database

how does it works?
    After we initialize our project with alembic, two new items will appear in our directory
        - alembic.init
        - alembic directory
    these are created automatically by alembic so we can upgrade, downgrade and keep integrity of our application

    alembic.ini file 
        - File that alembic looks for when invoked
        - Contains a bunch of configuration information for alembic that we are able to change to match our project
    alembic directory
        - Has all environment properties for alembic
        - Holds all revisions of you application
        - here we can call the migrations for upgrading and downgrading



Using Alembic
    alembic init alembic -> here second alembic is a name and can be anything
        this creates everything we need to use alembic

    Alembic revision
        alembic revision is how we create a new alembic file where we can add some type of database upgrade

        when we run
            alembic revision -m "create phone number col on users table"
        it creates a new file where we can write the upgrade code

        each new revision will have a revision Id, it unique id for that particular data migration

    Alembic Upgrade
        inside the newly created revision file we will write the code to perform the upgrade like
            def upgrade() -> None
                op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))

        it will create a new column in the user table 
        the previous data within the database table does not change

    to run the upgrade migration
        alembic upgrade <revision id>

    alembic downgrade
        to downgrade(revert back the changes) we need to add the downgrade code in the revision file
            def downgrade() -> None:
                op.drop_column('users', 'phone_number')
    
        it will remove the column phone_number from the table 
        the data of the table will not change unless it was on the upgraded column "phone_number" because it will be deleted
    
    ro run the downgrade migration
        alembic downgrade -1

        it will revert the last migration
    