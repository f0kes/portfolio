This project is a sophisticated Dota 2 replay parser and state tracker, designed to analyze and extract detailed game information from Dota 2 replay files. It processes replay data in real-time, tracking the state of heroes, units, and game events throughout the match.

Key Features:

1. Real-time replay parsing: Processes Dota 2 replay files as they are streamed.
2. Comprehensive game state tracking: Monitors heroes, units, abilities, items, and game events.
3. Vision simulation: Tracks unit visibility based on game rules.
4. RESTful API: Provides parsed data through a web service interface.
5. Entity mapping and caching: Efficiently maps game entities to unique identifiers.
6. Scalable architecture: Designed to handle multiple concurrent parsing requests.

Key Technologies:

1. Kotlin: Primary programming language, offering modern features and Java interoperability.
2. Clarity: Library for parsing Dota 2 replay files.
3. Ktor: Kotlin-based asynchronous web framework for building the API.
4. Redis: In-memory data structure store used for caching and fast data retrieval.
5. Protocol Buffers: Efficient binary serialization format for game state data.
6. Koin: Lightweight dependency injection framework for Kotlin.
7. Kotlinx.serialization: Kotlin multiplatform serialization library.
8. Gradle: Build automation tool for managing dependencies and building the project.
9. Docker: Containerization for easy deployment and scaling.

This project demonstrates proficiency in game data analysis, real-time data processing, efficient data structures, and building scalable web services. It showcases the ability to work with complex, domain-specific data formats and implement game logic in a high-performance environment.