import setuptools

long_description="about\n--\nThis is a python package for orbiting turtles in python's turtle package. all you need to use is the orbit function and it will move your turtle in an orbiting motion for as long as you loop it.\nthis package comes with 2 functions:\n\norbit function:\n--\norbit(turt,originx,originy,radius,dangle,angle=0)\n\nturt is the turtle to orbit\n\noriginx and originy is what its orbiting around. \n\nradius is how far from the origin the orbit it is\n\ndangle is the delta angle, positive for counterclockwise, negetive for clockwise. the more the faster.\n\nangle is the current angle. if you do not enter an angle, it will make an angle variable in your turtle (turtlename.angle) and will use that.\n\nradians function\n--\nrad(x)\n\nx is the number to convert to radians (from degrees)."

setuptools.setup(
    name="pyturtleorbit", # Put your username here!
    version="1.2.1", # The version of your package!
    author="Seamus Donahue", # Your name here!
    author_email="thedarkknite10@gmail.com", # Your e-mail here!
    description="A package for orbiting turtles in python", # A short description here!
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://repl.it/@SeamusDonahue/pyorbit#pyorbit_project/setup.py", # Link your package website here! (most commonly a GitHub repo)
    packages=["pyturtleorbit"], # A list of all packages for Python to distribute!
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Enter meta data into the classifiers list!
    python_requires='>=3.6', # The version requirement for Python to run your package!
		License="MIT",
)
