import os
import logging

from urllib.parse import quote_plus

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from dotenv import load_dotenv


class MongoDBClient:

    def __init__(self):
        """Initialize the MongoDB client with configuration from environment variables.

        This constructor loads environment variables for the MongoDB connection,
        sets up logging, and initializes instance variables for the MongoDB client.
        """
        load_dotenv()  # Load environment variables
        logging.basicConfig(level=logging.DEBUG)
        self.__logger = logging.getLogger(__name__)
        self.__mongo_client = None
        self.__host = os.getenv('MONGO_DB_URL', 'localhost')
        self.__username = os.getenv('MONGO_INITDB_ROOT_USERNAME', '')
        self.__password = os.getenv('MONGO_INITDB_ROOT_PASSWORD', '')
        self.__port = int(os.getenv('MONGO_INITDB_ROOT_PORT', 27017))

    async def get_client(self):
        """Setup and return an asynchronous MongoDB client.

        If the MongoDB client is already established, it returns the existing client.
        Otherwise, it creates a new client, tests the connection, and logs the result.

        Returns:
            AsyncIOMotorClient: An instance of the MongoDB client.
        
        Raises:
            ConnectionFailure: If unable to connect to MongoDB.
            ConfigurationError: If there is a configuration error during connection.
            Exception: For any other unexpected errors during connection.
        """
        if self.__mongo_client:
            return self.__mongo_client
        try:
            endpoint = f'mongodb://{quote_plus(self.__username)}:'\
                       f'{quote_plus(self.__password)}@{self.__host}:{self.__port}'
            self.__logger.info("Connecting to MongoDB at %s:%s", self.__host, self.__port)
            self.__mongo_client = AsyncIOMotorClient(endpoint)
            # Test the connection with a ping
            await self.__mongo_client.admin.command('ping')
            self.__logger.info("Successfully connected to MongoDB.")
        except (ConnectionFailure, ConfigurationError) as e:
            self.__logger.error("Failed to connect to MongoDB: %s", str(e))
            raise
        except Exception as e:
            self.__logger.error("An unexpected error occurred: %s", str(e))
            raise
        return self.__mongo_client

    async def close(self):
        """Close the MongoDB connection.

        This method closes the connection to the MongoDB client if it exists,
        logging the closure of the connection.
        """
        if self.__mongo_client:
            self.__logger.info("Closing MongoDB connection.")
            self.__mongo_client.close()  # Cleanly close the MongoDB connection
            self.__mongo_client = None

    async def __aenter__(self):
        """Enter the asynchronous runtime context.

        This method establishes the MongoDB connection and returns the MongoClient instance
        for usage within a context manager.

        Returns:
            AsyncIOMotorClient: An instance of the MongoDB client.
        """
        await self.get_client()  # Establish the connection
        return self.__mongo_client  # Return the MongoClient instance for usage

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the asynchronous runtime context and close the MongoDB connection.

        This method ensures that the MongoDB connection is closed when exiting the context.

        Args:
            exc_type: The exception type (if any) that caused the context to exit.
            exc_val: The exception value (if any) that caused the context to exit.
            exc_tb: The traceback object (if any) that caused the context to exit.
        """
        await self.close()
