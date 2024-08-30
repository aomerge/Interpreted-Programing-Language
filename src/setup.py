## creamos una clase para el manejo y la inicializacion de mi Lpp 
class Lpp:
    def __init__(self, nombre):
        self.nombre = nombre
        self.version = "0.0.1"
        self.author = "Jhonatan"
        self.author_email = ""
        self.url = "http://www.jhonatan.com"
        self.description = "Lpp Distribution Utilities"
        self.long_description = self.__readme()
        self.license = "MIT"
        self.packages = ["lpp"]
        self.install_requires = ["requests"]
        self.keywords = ["lpp", "lppd", "lppdistribucion", "lppdistribucionpaquetes"]
        self.classifiers = [
            "Development Status :: 1 - Planning",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: Spanish",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.8",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ]

