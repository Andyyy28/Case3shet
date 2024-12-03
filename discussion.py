from datetime import datetime
from person import Person
from course import Course

class DiscussionThread:
    def __init__(self, course: 'Course', title: str, creator: 'Person'):
        self.course = course  # The course associated with this discussion thread
        self.title = title
        self.creator = creator  # Person (could be Student or Instructor)
        self.posts = []  # List of posts (messages) in this thread
        self.timestamp = datetime.now()

    def display_thread(self) -> None:
        """Display the thread details with all posts."""
        print(f"Discussion Thread: {self.title}")
        print(f"Created by: {self.creator.name} on {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Course: {self.course.course_name} (Code: {self.course.course_code})")
        print("Posts:")
        for post in self.posts:
            print(f"- {post['person']} ({post['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}): {post['message']}")

    def add_post(self, person: 'Person', message: str) -> None:
        """Add a post to the thread."""
        if not message.strip():
            print("Cannot post an empty message.")
            return
        post = {
            'person': person.name,
            'timestamp': datetime.now(),
            'message': message
        }
        self.posts.append(post)
        print(f"Post added by {person.name}: {message}")
