"""
Alpha Discord Bot Version Information
Pterodactyl Panel Compatible Version
"""

__version__ = "1.0.1"
__author__ = "AI Assistant"
__description__ = "Professional Discord Management Solution"
__platform__ = "Pterodactyl Panel"
__status__ = "Production Ready"

# Version History
VERSION_HISTORY = {
    "1.0.0": {
        "date": "2025-08-10",
        "description": "Initial release with all core features",
        "features": [
            "Discord Management Module (announcements, messaging, role management)",
            "Time Management Module (timezone support, clock in/out system)",
            "Comprehensive Logging Module (all server activities)",
            "Professional UI with slash commands",
            "Smart user lookup without pinging",
            "Modular architecture for easy feature additions"
        ]
    },
    "1.0.1": {
        "date": "2025-08-10",
        "description": "Enhanced privacy with ephemeral commands",
        "features": [
            "All slash commands now private to user (ephemeral)",
            "Discord Management Module (announcements, messaging, role management)",
            "Time Management Module (timezone support, clock in/out system)",
            "Comprehensive Logging Module (all server activities)", 
            "Professional UI with slash commands",
            "Smart user lookup without pinging",
            "Modular architecture for easy feature additions"
        ]
    }
}

def get_version_info():
    """Get current version information"""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "platform": __platform__,
        "status": __status__,
        "release_date": VERSION_HISTORY[__version__]["date"],
        "features": VERSION_HISTORY[__version__]["features"]
    }

def get_deployment_info():
    """Get deployment-specific information"""
    return {
        "platform": __platform__,
        "status": __status__,
        "python_compatible": "3.8+",
        "discord_py_version": "2.3.0+",
        "container_ready": True,
        "modules_count": 4,
        "commands_count": "17+",
        "deployment_type": "24/7 Hosting"
    }
