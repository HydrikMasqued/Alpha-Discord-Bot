"""
Alpha Discord Bot Version Information
"""

__version__ = "1.0.0"
__author__ = "AI Assistant"
__description__ = "Professional Discord Management Solution"

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
    }
}

def get_version_info():
    """Get current version information"""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "release_date": VERSION_HISTORY[__version__]["date"],
        "features": VERSION_HISTORY[__version__]["features"]
    }
