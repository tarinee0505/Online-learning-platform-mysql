from django.contrib.auth.models import User
from app.models import Course, Module

def create_sample_course():
    # Create or get instructor
    instructor, created = User.objects.get_or_create(
        username='instructor',
        defaults={
            'email': 'instructor@example.com',
            'is_staff': True
        }
    )
    
    # Create course
    course = Course.objects.create(
        title='Python Programming Basics',
        slug='python-programming-basics',
        description='Learn the fundamentals of Python programming.',
        instructor=instructor,
        price=99.99,
        duration=8,
        is_active=True,
        is_featured=True
    )
    
    # Create modules
    modules = [
        {
            'title': 'Introduction to Python',
            'description': 'Basic Python concepts and setup',
            'content': 'Learn about Python installation and basic syntax.',
            'order': 1
        },
        {
            'title': 'Variables and Data Types',
            'description': 'Understanding Python data types',
            'content': 'Explore different data types in Python.',
            'order': 2
        },
        # Add more modules as needed
    ]
    
    for module_data in modules:
        Module.objects.create(
            course=course,
            **module_data
        )
    
    return course

# Run this function to create a sample course
if __name__ == '__main__':
    course = create_sample_course()
    print(f"Created course: {course.title}") 