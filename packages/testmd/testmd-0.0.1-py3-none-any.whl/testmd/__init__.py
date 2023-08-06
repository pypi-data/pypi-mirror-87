#!/usr/bin/env python3
"""
Checks a directory of markdown files for lint
"""

import argparse
import datetime
import os
import sys
import configparser
import frontmatter
import logging


class TestMd:
    """
    Consumes a markdown file and provides methods reporting on it.
    This particularly relates to items contained within the markdown yaml frontmatter
    """

    def __init__(self, md_file_name, config):
        self.exit_status = 0
        self.md_file_name = md_file_name
        self.config = config
        with open(md_file_name) as input_file:
            self.article = frontmatter.load(input_file)
        self.current_date = datetime.date.today()

    def run_tests(self):
        """ Runs the tests defined in the config file """
        logging.debug("Testing: %s", self.md_file_name)
        for test in self.config:
            if test != "DEFAULT":
                self.check_key_exists(test)
                if self.exit_status == 0:
                    self.check_type(test)
                    self.check_param_options(test)
                self.check_expiry(test)
                    

    def check_key_exists(self, test):
        """ Check that the key descibed in the test exists """
        logging.debug("(Test: %s) Checking key exists", test)
        try:
            self.article[self.config[test]["name"]]
        except KeyError:
            logging.error(
                "(Test: %s) parameter %s not defined - %s",
                test,
                self.config[test]["name"],
                self.md_file_name,
            )
            self.exit_status = 1

    def check_type(self, test):
        """ Check the key's type against the test spec """
        logging.debug("(Test: %s) Checking type", test)
        try:
            article_data = self.article[self.config[test]["name"]]
        except KeyError:
            logging.error(
                "( Test: %s ) parameter %s not defined - ",
                test,
                self.config[test]["name"],
                self.md_file_name,
            )
            self.exit_status = 1
            return
        if self.config[test]["type"] == "string":
            if not isinstance(article_data, str):
                logging.error(
                    "(Test: %s) parameter %s is not a string - %s",
                    test,
                    self.config[test]["name"],
                    self.md_file_name,
                )
                self.exit_status = 1
        if self.config[test]["type"] == "date":
            if not isinstance(article_data, datetime.date):
                logging.error(
                    "(Test: %s) parameter %s is not a date - %s",
                    test,
                    self.config[test]["name"],
                    self.md_file_name,
                )
                self.exit_status = 1

    def check_expiry(self, test):
        """ With a type is a date, check for an age and then test the date is not older """
        logging.debug("(Test: %s) Checking expiry", test)
        if self.config[test]["type"] == "date":
            logging.debug("(Test: %s) Type is date", test)
            try:
                article_date = self.article["date"]
            except KeyError:
                logging.error("(Test: %s) No date defined - %s", test, self.md_file_name)
                self.exit_status = 1
                return
            review_date = datetime.datetime.now() - datetime.timedelta(
                days=int(self.config[test]["age"])
            )
            logging.debug("(Test: %s) Review date: %s - %s", test, review_date, self.md_file_name)
            if datetime.datetime.combine(article_date, datetime.time(0)) < review_date:
                logging.error(
                    "(Test: %s) Document expired - %s", test, self.md_file_name
                )
                self.exit_status = 1
        else:
            logging.debug("(Test: %s) type is not date", test)

    def check_param_options(self, test):
        """ If the key has a list of options in the test spec, test that the file matches one """
        logging.debug("(Test: %s) Checking param options", test)
        if self.config[test]["type"] == "string":
            try:
                options = self.config[test]["options"].splitlines
            except KeyError:
                logging.error("(Test: %s) No options defined", test)
                self.exit_status = 1
                return
            if self.article[self.config[test]["name"]] not in options:
                logging.error(
                    "( Test: %s ) paarmeter %s is not in options - %s",
                    test,
                    self.config[test]["name"],
                    self.md_file_name,
                )
