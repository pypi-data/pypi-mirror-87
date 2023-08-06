from setuptools import setup, find_packages 
  
with open('requirements.txt') as f: 
    requirements = f.readlines() 
  
long_description = 'Command Line Utility to search for coding related queries.' 
  
setup( 
        name ='howcani', 
        version ='0.0.1', 
        author ='Rahul D Shetty', 
        author_email ='35rahuldshetty@gmail.com', 
        url ='https://github.com/rahuldshetty/howcani', 
        description ='CLI Query Searcher', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='MIT', 
        packages = find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                'howcani = howcani:main'
            ] 
        }, 
        classifiers =( 
            "Programming Language :: Python :: 3", 
            "License :: OSI Approved :: MIT License", 
            "Operating System :: OS Independent", 
        ), 
        keywords ='rahuldshetty howcani search stackoverflow google', 
        install_requires = requirements, 
        zip_safe = False
) 
