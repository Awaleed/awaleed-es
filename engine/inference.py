"""
Inference Engine to run the forward and backward chaining on the parsed
KnowledgeBase and ClauseBase
"""

import os
import secrets

from engine.components.knowledge import Knowledge
from engine.logger.logger import Log
from engine.parser.knowledgeParser import KnowledgeBaseParser
from engine.util.constants import USER_INPUT_SEP, AVATAR, PERCENT_MATCH
from engine.util.utilities import sortDictionary


class Inference:
    """
    Inference parses the input files and creates KnowledgeBase and ClauseBase that can be
    used for forward and backward chaining

    Attributes
    -----------
    __knowledgeParser : KnowledgeBaseParser
        parser to parse the knowledge file into objects
    __knowledgeBase : list
        list of parsed Knowledge objects
    __verbose : bool
        to print the matched values percents
    __method : str
        values accepted

            forward : run forward chaining
            backward : run backward chaining

    """

    def __init__(self):
        self.FORWARD = "forward"
        self.BACKWARD = "backward"

        self.__knowledgeParser = KnowledgeBaseParser()

        self.__knowledgeBase = None
        self.__verbose = None
        self.__method = None

    def startEngine(self, knowledgeBase, verbose=False, method="forward"):
        """
        Read the files to parse and other options. Initialize the parsers and get the parsed values

        Parameters
        ----------
        knowledgeBase : str
            name and path of the file
        verbose : bool, default=False
            to print extra details
        method : str, default="forward"
            method to run on

        """
        if not os.path.isfile(knowledgeBase):
            Log.e(f"The knowledge file {knowledgeBase} does not exists.")
        Log.d("Parsing the files to generate a Knowledge Base...")

        self.__knowledgeBase = self.__knowledgeParser.getKnowledgeBase(
            knowledgeBase)
        self.__verbose = verbose
        self.__method = method

    def inferenceResolve(self, userInput, verbose, method):
        self.__verbose = verbose
        self.__method = method
        return self.__inferenceResolve(userInput)

    def __inferenceResolve(self, userInput):
        """
        Run the inference on the user input for each clause. Method attribute determines
        the method being used

        Parameters
        ----------
        userInput : str
            input from the user

        Returns
        -------
        tuple
            bool : True for finding a match and string : A formatted string with target and percentage

        """
        userInputs = userInput.split(USER_INPUT_SEP)
        userKnowledge = Knowledge()

        # creating a knowledge base of the user input
        for userIn in userInputs:
            userKnowledge.addRule("user", userIn.strip())

        # run inference with selected method
        if self.__method == "forward":
            return self.__runForwardChain(userKnowledge)
        else:
            return self.__runBackwardChain(userKnowledge)

    def __runForwardChain(self, userBase: Knowledge):
        """
        Running forward chaining.Steps are as follows :

            1. Match each user rule with all the rules for each Knowledge target
            2. Calculate the percentage for each target
            3. Return the output for the percent that satisfies the Min percent
            4. If verbose is True, print all matches with percentages

        Parameters
        ----------
        userBase : Knowledge
            Knowledge object created by parsing the user input

        Returns
        -------
        tuple
            bool : True denoting match found; str : formatted target name and percentage
        """
        matchesRules = dict()

        # getting each knowledge from the base
        for knowledge in self.__knowledgeBase:
            match = 0

            # comparing each rule
            for rule in knowledge.getRules():
                for userRule in userBase.getRules():
                    if rule == userRule:
                        match += 1

            # adding the percent of match for each target
            matchesRules[knowledge.getTarget()] = (
                match / len(knowledge.getRules())) * 100

        # high percentage is returned based on satisfaction of MATCH
        matchesRules = sortDictionary(matchesRules)

        if self.__verbose:
            res = list()
            sure = False
            for target, percent in matchesRules.items():
                if percent >= PERCENT_MATCH:
                    sure = True
                res.append({"target": target, "percent": percent})
                Log.d(f"Target :: {target} --->  Matched :: {percent}")
            print()
            return {"image": self.makeImage(sure), "sure": sure, "value": res}

        # returning the first match if it greater than the MIN
        for target, percent in matchesRules.items():
            if percent >= PERCENT_MATCH:
                return {"image": self.makeImage(True), "sure": True, "value": [{"target": target, "percent": percent}]}
            else:
                return {"image": self.makeImage(False), "sure": False, "value": [{"target": target, "percent": percent}]}
        return {"image": self.makeImage(False), "sure": False, "value": []}

    def __runBackwardChain(self, userBase: Knowledge):
        """
        Running forward chaining.Steps are as follows :

            1. Scan the Knowledge Base rules with the user rule
            2. When match is found, save the Knowledge target as new target
            3. Run match on the selected targets
            4. Return the output based on the Min percent

        Parameters
        ----------
        userBase : Knowledge
            Knowledge object created by parsing the user input

        Returns
        -------
        tuple
            bool : True denoting match found; str : formatted target name and percentage
        """
        matchedTargets = list()
        matchesRules = dict()

        # finding initial target
        for knowledge in self.__knowledgeBase:
            for rule in knowledge.getRules():
                for userRule in userBase.getRules():
                    # rule match target acquired
                    if rule == userRule:
                        matchedTargets.append(knowledge)
                        break

        # running matching on the selected targets
        for matchedTarget in matchedTargets:
            match = 0
            for rule in matchedTarget.getRules():
                for userRule in userBase.getRules():
                    if rule == userRule:
                        match += 1

            # saving the target with its percent match
            matchesRules[matchedTarget.getTarget()] = (
                match / len(matchedTarget.getRules())) * 100

        # sorting the matched rules by the percentages
        matchesRules = sortDictionary(matchesRules)

        if self.__verbose:
            res = list()
            sure = False
            for target, percent in matchesRules.items():
                if percent >= PERCENT_MATCH:
                    sure = True
                res.append({"target": target, "percent": percent})
                Log.d(f"Target :: {target} --->  Matched :: {percent}")
            print()
            return {"image": self.makeImage(sure), "sure": sure, "value": res}

        # returning the highest matches target if is greater than the MIN
        for target, percent in matchesRules.items():
            if percent >= PERCENT_MATCH:
                return {"image": self.makeImage(True), "sure": True, "value": [{"target": target, "percent": percent}]}
            else:
                return {"image": self.makeImage(False), "sure": False, "value": [{"target": target, "percent": percent}]}
        return {"image": self.makeImage(False), "sure": False, "value": []}

    def makeImage(self, sure: bool):
        foundIt = ["https://media1.giphy.com/media/6omlIrIZREyoP3VGG4/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media0.giphy.com/media/BzT8yem5qT2j2MejiE/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media3.giphy.com/media/xUNda00lYcxvsyAXm0/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media4.giphy.com/media/WmiP6dkV4jSIivt36x/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media2.giphy.com/media/IS9LfP9oSLdcY/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media2.giphy.com/media/8AdlIamKVYo084YL4H/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media0.giphy.com/media/LNqiRp9njyVQim3pEG/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media3.giphy.com/media/Nl5LerAy1PswVczmSs/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media3.giphy.com/media/l4Ep8vfXfBYMPU38k/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media2.giphy.com/media/l0HlLJV0F2hhl0iGs/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media3.giphy.com/media/dvfKPWMsNdDIZjVVIE/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media3.giphy.com/media/l0HlQsta67RntNEtO/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media2.giphy.com/media/3o6ZtpwN7d8sHfpxjq/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media4.giphy.com/media/WRoKv6KVZA0i5RvL6q/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media0.giphy.com/media/3o6Zt5EdmsSfyhOBH2/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media3.giphy.com/media/26Ff7c9cWqW0KdEqs/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media4.giphy.com/media/xT5LMGvqMv62a1PNTO/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media3.giphy.com/media/l378ohFdsetxucAMM/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media1.giphy.com/media/tcCjCouFDBHUOY7gDB/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media2.giphy.com/media/3o6ZtbKuHUgywWZciY/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media2.giphy.com/media/xUNd9B0MR1VJq2CMfK/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media1.giphy.com/media/l4EoYblJQzeCR7sOs/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media1.giphy.com/media/LOLMSQ6CO5KLPjFtC8/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media4.giphy.com/media/3o6nUVOWPXScfYFeBW/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media4.giphy.com/media/3o6Mb9p4aYXJdtWoDe/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media1.giphy.com/media/xT1R9B9UtcW8QzqlQQ/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media2.giphy.com/media/xUPOqeLMPlyc1O2oE0/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media0.giphy.com/media/xUNd9NwysfGCrQqFfG/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media1.giphy.com/media/xT1R9D1v9ll3IL8QQE/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media3.giphy.com/media/l0HlDxWbDj8bQPM1W/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media2.giphy.com/media/3o6Zt78VuYjOHh6Ho4/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media1.giphy.com/media/JseEqKOkHeDfSUJneQ/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media4.giphy.com/media/l0HlFKq01wp3yOmOs/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media0.giphy.com/media/l0HlQqjty0Lkz1JVm/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media4.giphy.com/media/YPQ5w5BKVgvy4RlOjC/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media2.giphy.com/media/l4Ep0R2B18J5PHT6U/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media4.giphy.com/media/26Ff3FoWSexdzVtew/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media0.giphy.com/media/l1IYf5koPLuZvpIw8/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media0.giphy.com/media/l4Epeur5EnrTsPV2o/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media2.giphy.com/media/l4EpgjhpMFkVDU0gg/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media1.giphy.com/media/xUNd9PguujogkhJXZC/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media3.giphy.com/media/ouk2ttrPlja5a/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media0.giphy.com/media/xUySTT4jM3fv57gFEs/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media3.giphy.com/media/3o6wruJCSdNJIZKOYg/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media0.giphy.com/media/xUPOqBitngO0s3PiQ8/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media3.giphy.com/media/26Ff9thO8eqdnqhhu/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media2.giphy.com/media/xT1Ra1ozTIHCYRIdi0/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media2.giphy.com/media/l0ErOfPOfBTcDlrRS/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g",

                   "https://media0.giphy.com/media/l0ErJnNajBFpkWyPe/giphy.gif?cid=e71a7766wx4177vknipmasey85k7ty5i7bpnk9xmlyem9jhg&rid=giphy.gif&ct=g", ]

        notFindIt = ["https://media3.giphy.com/media/BMtGb8JSk2Ln1cnPMA/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media2.giphy.com/media/ANbD1CCdA3iI8/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media2.giphy.com/media/ZFhhpKngh5QfcmhIDF/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media1.giphy.com/media/5t9wJjyHAOxvnxcPNk/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media1.giphy.com/media/l0IyhLWvcoVWzIM5W/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media2.giphy.com/media/sqbnHI0hNHC7u/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media4.giphy.com/media/3og0IF7LxXgYt4X9Bu/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media1.giphy.com/media/Ogq017TWp45JadcpIK/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media3.giphy.com/media/xT8qB3V08emk70OLrG/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media3.giphy.com/media/Jp3tixBJ0YERe4PXig/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media4.giphy.com/media/h1u4Dpc1xRrrN2Jptc/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media3.giphy.com/media/3o7TKAqccE1aEOP2H6/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media4.giphy.com/media/9xijGdDIMovchalhxN/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media1.giphy.com/media/yhc3VVqX2wBdnHKyqG/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media2.giphy.com/media/3o6ZtnCmudwAQCLmhy/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media2.giphy.com/media/MCR7hOiqQcaOoUvXcX/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media3.giphy.com/media/l396T0MZ9QKZlw772/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media1.giphy.com/media/eGmKeueVnk31yCRQW5/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media2.giphy.com/media/ZdZsyik26Z1YRMEksr/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media4.giphy.com/media/Tk0mQHwaCSZAtCLpyN/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media0.giphy.com/media/3o6ZtmGxr1sxM7pP1e/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media2.giphy.com/media/1Bd8m7yqGsFwVOVQFE/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media3.giphy.com/media/xUySTAtNXUy9tyndbq/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media4.giphy.com/media/69jAWVExLA8zYdMKWZ/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media4.giphy.com/media/8Bkb0njbHzXHL43UMS/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media4.giphy.com/media/fzIFufqmzoS5lif6FQ/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media3.giphy.com/media/puOukoEvH4uAw/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media0.giphy.com/media/l2SpTOuicRRVJVzs4/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media4.giphy.com/media/NUerTUMGyYyKoUl0pK/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media4.giphy.com/media/1SFkiALCLQFNK/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media3.giphy.com/media/hSLn2rOC2R34WKX0g4/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media4.giphy.com/media/l3vQWTbh8IxXGBM7S/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media0.giphy.com/media/2A841rbNEA1Tq0ofca/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media2.giphy.com/media/xUn3C0FedzfGl8ndaU/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media4.giphy.com/media/3ohzdMcizKma0QB6SY/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media1.giphy.com/media/lzzwvdi10plDy/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media0.giphy.com/media/Zd6Mf1dQNeYkQHEuzA/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media3.giphy.com/media/5YulXQD6c9XygnCuRN/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media3.giphy.com/media/dWT9rF7VqGhqX2jQZ0/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media2.giphy.com/media/xUNd9QgdlkXCn9325G/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media1.giphy.com/media/1lyiSfMXWq7QBPNSY1/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media4.giphy.com/media/3o8dFiXShIJ3Yjx3JC/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media3.giphy.com/media/xI5dVJKpKLzK8/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media1.giphy.com/media/1Af6W0bLi9udTnRqWu/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media4.giphy.com/media/7NFUmCZR15pof4YUrz/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media4.giphy.com/media/3oEjHLS6Va8qdALZCM/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media1.giphy.com/media/QMhVP5ihR0KS4/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media4.giphy.com/media/QVxYlTPA2xrs1uvNd0/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media2.giphy.com/media/xUPGcgOeRrKLVc6K0o/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",

                     "https://media2.giphy.com/media/1fgeF4RrCUzIO1afvr/giphy.gif?cid=e71a7766ks4qsmhm1fso0kkkm0e7lfyodfbl5l5miha7aax0&rid=giphy.gif&ct=g",
                     ]
        r = None
        if(sure):
            r = secrets.choice(foundIt)
        else:
            r = secrets.choice(notFindIt)
        return r
