import os
import re


class Parser:

    def __init__(self, file):
        file_content = self.__read_file(file)
        text_packages = file_content.split("\n\n")
        if len(text_packages[0]) > 0:
            self.dict_packages = [self.__parse_to_dict(text_package) for text_package in text_packages]
            self.package_names = [dict_package["package"] for dict_package in self.dict_packages]
            self.package_info = {}
            for package in self.dict_packages:
                package = self.__clean_package(package)
                self.package_info[package.get("name")] = package["info"]

    @staticmethod
    def __read_file(filename):
        if type(filename) is str and os.path.exists(os.path.dirname(filename)):
            with open(filename, "r") as f:
                content = f.read().strip()
            return content
        else:
            print("Filename is not string or path does not exist.")

    @staticmethod
    def __parse_to_dict(package_text):
        """Parses a package from the file to a dictionary"""

        # Matches field names up to the colon character
        split_regex = re.compile(r"^[A-Za-z-]+:", flags=re.MULTILINE)
        keys = [key[:-1].lower() for key in split_regex.findall(package_text)]

        # Gets values for each key. First split is 
        values = [value.strip() for value in re.split(split_regex, package_text)[1:]]
        # Composing initial package info dict
        if len(values) > 0:
            pkg_dict = dict(zip(keys, values))

            # Remove version
            split_regex = re.compile(r"\(.*?\)", flags=re.MULTILINE)
            if pkg_dict.get("depends") is not None:
                pkg_dict["depends"] = "".join(re.split(split_regex, pkg_dict.get("depends")))
            return pkg_dict
        else:
            raise ValueError("file or text don't match Debian Control File schema")

    def __clean_package(self, package):
        """Cleans up raw parsed package information and filters unneeded"""
        package_name = package.get("package")
        description = package.get("description")
        str_depends = package.get("depends")

        depends = self.__format_depends(str_depends)
        reverse_depends = self.__get_reverse_depends(package_name)

        package_info = {
            "description": description,
            "depends": depends,
            "reverse_depends": reverse_depends,
        }

        return {"name": package_name, "info": package_info}

    def __format_depends(self, str_depends):
        """Removes version and splits dependencies and alternatives"""
        depends = []
        if str_depends is not None:
            # Creates an array for each group of alternative dependencies
            for alt_depends in str_depends.split(","):
                depends.append([(alt_depend.strip(),
                                 alt_depend.strip() in self.package_names)
                                for alt_depend in alt_depends.split("|")])

        return depends

    def __get_reverse_depends(self, package_name):
        """Gets the names of the packages that depend on the given package"""
        reverse_depends = []
        for dict_package in self.dict_packages:
            package_depends = dict_package.get("depends")
            if package_depends is not None:
                package_depends = [package.strip() for package in package_depends.replace('|', ',').split(",")]

                if package_name in package_depends:
                    reverse_depends.append(dict_package["package"])

        return reverse_depends

    def get_package_names(self):
        return self.package_names

    def get_package_info(self, package):
        return self.package_info[package] if package in self.package_info else None
