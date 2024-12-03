from e_learning_environment import E_Learning_Environment
from platform_admin import PlatformAdmin

if __name__ == "__main__":
    try:
        # Initialize the PlatformAdmin and load data
        platform_admin = PlatformAdmin()
        
        # Check if load_data method exists
        if hasattr(platform_admin, 'load_data'):
            platform_admin.load_data('data.json')  # Load data from JSON
        else:
            raise AttributeError("PlatformAdmin does not have a 'load_data' method.")
        # Initialize the E-Learning Environment
        e_learning_system = E_Learning_Environment()

        # Ensure platform_admin can be set in E-Learning system
        if hasattr(e_learning_system, 'platform_admin'):
            e_learning_system.platform_admin = platform_admin
        else:
            raise AttributeError("E_Learning_Environment does not have a 'platform_admin' property or method.")
        
        # Ensure the set_courses method exists and passes the courses to E-Learning system
        if hasattr(e_learning_system, 'set_courses'):
            # Check if platform_admin has 'courses', adjust if it's a method
            if hasattr(platform_admin, 'courses'):
                e_learning_system.set_courses(platform_admin.courses)  # Assuming platform_admin has a courses attribute
            elif hasattr(platform_admin, 'get_courses'):
                e_learning_system.set_courses(platform_admin.get_courses())  # Call if it's a method
            else:
                raise AttributeError("PlatformAdmin does not have a 'courses' attribute or 'get_courses' method.")
        else:
            raise AttributeError("E_Learning_Environment does not have a 'set_courses' method.")
        
        # Start the main menu
        e_learning_system.main_menu()

    except AttributeError as e:
        print(f"AttributeError: {e}")  # More specific error handling
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")  # Handle missing file
    except Exception as e:
        print(f"An unexpected error occurred: {e}")  # Generic error for all other cases