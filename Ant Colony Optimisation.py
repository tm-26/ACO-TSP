# TODO
# 1) Add for all EDGE_WEIGHT_TYPEs 🗸
# 2) Visit first city again after path is complete 🗸

import math  # Used for a multitude of computations
import random  # Used to randomly generate the first node


# Deceleration of global variables that are going to be used through out the program

lengthOfTour = []
currentTour = 0
currentTourList = []
variables = {
    "cityi": 0,
    "cityj": 0,
    "pheromone": 1,
    "visibility": 0,
    "sumofpheromone": 0
}
variablesList = []


def nextnode(currentcity, numberofcities, visitedNodes, reductionrateofpheromone, quantityofpheromone,
             distancelist, alpha, beta, last, firstcity):
    bestNodes = []
    global lengthOfTour
    global currentTour
    global currentTourList
    distances = []

    probability = []
    global variables
    i = 0
    numerators = []
    probabilitysum = 0

    # First we make sure that our tour is not complete

    if not last:
        # For all cities
        while i < numberofcities:
            # That have not been visited
            if i not in visitedNodes:
                variables["cityi"] = currentcity
                variables["cityj"] = i
                # Find distance to that city:
                citycount = 0
                found = False
                while not found:
                    # Traverse through the list until you find city i and city j
                    if (currentcity == (distancelist[citycount])["cityi"] and i == (distancelist[citycount])["cityj"]) \
                            or (currentcity == ((distancelist[citycount])["cityj"]) and i == (distancelist[citycount])[
                                "cityi"]):
                        bestNodes.append(i)
                        currentdistance = (distancelist[citycount])["distance"]
                        distances.append(currentdistance)
                        # While you're at it, find the visibility as well
                        (variablesList[citycount])["visibility"] = 1 / currentdistance

                        numerators.append((math.pow((variablesList[citycount])["pheromone"], alpha) * math.pow((variablesList[citycount])["visibility"], beta)))
                        probabilitysum = probabilitysum + numerators[-1]

                        pheromone = quantityofpheromone / currentdistance
                        (variablesList[citycount])["sumofpheromone"] = (variablesList[citycount])["sumofpheromone"] + pheromone
                        (variablesList[citycount])["pheromone"] = reductionrateofpheromone * (variablesList[citycount])["pheromone"] + variables["sumofpheromone"]

                        found = True
                    citycount += 1
            i += 1
        j = 0
        while j < len(numerators):
            probability.append(numerators[j] / probabilitysum)
            j += 1

        if round(sum(probability), 4) == 1:
            Max = probability.index(max(probability))
            currentTour = currentTour + distances[Max]
            currentTourList.append(distances[Max])
            return bestNodes[Max]
        else:
            print("An error has occurred, sum of probabilities not equal to 1")
            print("Exiting Program")
            exit(0)
    else:
        # If Tour is complete
        for fdistances in distancelist:
            if (fdistances["cityi"] == firstcity and fdistances["cityj"] == currentcity) or \
                    (fdistances["cityi"] == currentcity and fdistances["cityj"] == firstcity):
                currentdistance = fdistances["distance"]
                currentTour = currentTour + fdistances["distance"]

                pheromone = quantityofpheromone / currentdistance
                variables["sumofpheromone"] = variables["sumofpheromone"] + pheromone
                variables["pheromone"] = reductionrateofpheromone * variables["pheromone"] + variables["sumofpheromone"]
                numerators.append((math.pow(variables["pheromone"], alpha) * math.pow(variables["visibility"], beta)))
                probabilitysum = probabilitysum + numerators[-1]
                return firstcity


if __name__ == "__main__":

    # Start of parser

    file = open("TSPLIB.txt", "r")
    print("Opening TSPLIB")
    if not (file.mode == 'r'):
        print("Error: TSPLIB.tsp not found")
        exit()

    print("TSPLIB found and opened")
    print("--------------------------------------------------------------------")
    print(file.read())
    print("--------------------------------------------------------------------")
    print()

    file.seek(0)
    lines = file.read().splitlines()
    count = 0
    nodeNumber = []
    xCord = []
    yCord = []
    visited = []
    nodeCoordSectionFound = False
    typeFound = False
    lastCity = False
    weightType = ""
    hasNodes = False
    hasCoords = False
    distances = {
        "cityi": 0,
        "cityj": 0,
        "distance": 0
    }
    distanceList = []

    counterI = 0
    counterJ = 1

    i = 0
    while i < len(lines):
        currentLine = lines[i]
        if hasNodes:
            currentLine = "EDGE_WEIGHT_SECTION"
        elif hasCoords:
            currentLine = "NODE_COORD_SECTION"
        count += 1

        if currentLine.startswith("TYPE") and not typeFound and not hasCoords:
            typeFound = True
            current = currentLine.replace(" ", "")
            if current != "TYPE:TSP":
                print("The given file is not of the type TSP but rather:")
                print(currentLine)
                print("Do please note that the file will still be processed as if a TSP was entered")
        if (currentLine == "NODE_COORD_SECTION" or currentLine == "DISPLAY_DATA_SECTION") and not hasNodes:
            if weightType == "":
                print("Entered weight type is not defined, or is defined after the data. The file will be processed as "
                      "weight type EUC_2D")
            elif weightType == "EXPLICIT":
                print("EXPLICIT data found, converting '", currentLine, "' into 'EDGE_WEIGHT_SECTION' ")
                hasNodes = True
                continue
            counter = i
            while count <= len(lines):
                currentLine = lines[counter + 1]
                if currentLine.strip() == "EOF" or not currentLine:
                    break
                current = currentLine.split()
                nodeNumber.append(current[0])
                xCord.append(current[1])
                yCord.append(current[2])
                count += 1
                counter += 1
            nodeCoordSectionFound = True
        if currentLine == "EDGE_WEIGHT_SECTION" and not hasCoords:
            if weightType == "":
                print("Entered weight type is not defined, or is defined after the data. The file will be processed as "
                      "weight type EXPLICIT")
            elif weightType != "EXPLICIT":
                print("'", currentLine, "' found, converting into 'NODE_COORD_SECTION")
                hasCoords = True
                continue
            counter = i
            while count < len(lines):
                try:
                    currentLine = lines[counter + 1]
                except IndexError:
                    break
                if currentLine == "EOF" or not currentLine or currentLine == "DISPLAY_DATA_SECTION":
                    break
                current = currentLine.split()
                for distance in current:
                    distances["cityi"] = counterI
                    distances["cityj"] = counterJ
                    distances["distance"] = float(distance)
                    counterJ += 1
                    distanceList.append(distances.copy())

                    variables["cityi"] = counterI
                    variables["cityj"] = counterJ
                    variables["pheromone"] = 1
                    variables["visibility"] = 0
                    variables["sumofpheromone"] = 0

                    variablesList.append(variables.copy())
                counterI += 1
                counterJ = counterI + 1
                counter += 1
                nodeCoordSectionFound = True

        currentLine = "".join(currentLine.split())
        if currentLine.startswith("EDGE_WEIGHT_TYPE"):
            weightType = currentLine[17:]
            weightType = "".join(weightType.split())

            if weightType != "EUC_2D" and weightType != "CEIL_2D" and weightType != "GEO" and weightType != "EXPLICIT":
                print("Entered weight type is invalid, the file will be processed as weight type EUC_2D")
                weightType = "EUC_2D"
        if nodeCoordSectionFound:
            if not weightType.strip():
                print("Entered weight type is invalid, the file will be processed as weight type EUC_2D")
                weightType = "EUC_2D"
            break
        i += 1

    i = 0
    numberOfCities = len(nodeNumber)
    if weightType == "EXPLICIT":
        numberOfCities = counterI + 1

    if weightType != "EXPLICIT":
        while i < numberOfCities:
            nodeNumber[i] = float(nodeNumber[i])
            xCord[i] = float(xCord[i])
            yCord[i] = float(yCord[i])
            i += 1

    # End of Parser
    # Start of ACO algorithm

    # List of parameters
    alpha = 1
    beta = 4
    numberOfIterations = 100
    numberOfAnts = 100
    reductionRateOfPheromone = 0.5
    quantityOfPheromone = 100

    # List of variables
    iterationNum = 1
    antNumber = 1
    currentCity = 0
    firstCity = 0

    i = 0
    j = 1
    if weightType == "EUC_2D" or weightType == "CEIL_2D":
        while i <= numberOfCities:
            while j < numberOfCities:
                distances["cityi"] = i
                distances["cityj"] = j
                if weightType == "CEIL_2D":
                    distances["distance"] = int((math.sqrt(math.pow((xCord[i] - xCord[j]), 2) + math.pow((yCord[i] - yCord[j]), 2))))
                else:
                    distances["distance"] = (math.sqrt(math.pow((xCord[i] - xCord[j]), 2) + math.pow((yCord[i] - yCord[j]), 2)))
                distanceList.append(distances.copy())

                variables["cityi"] = i
                variables["cityj"] = j
                variables["pheromone"] = 1
                variables["visibility"] = 0
                variables["sumofpheromone"] = 0

                variablesList.append(variables.copy())

                j += 1
            i += 1
            j = i + 1
    elif weightType == "GEO":
        radiusOfEarth = 6378.137  # According to wikipedia's SI definition and proper documentation of tsp files
        while i < numberOfCities:
            lat1 = math.radians(xCord[i])
            while j < numberOfCities:

                latDif = math.radians(xCord[j] - xCord[i])
                lonDif = math.radians(yCord[j] - yCord[i])
                a = math.sin(latDif/2) * math.sin(latDif/2) + math.cos(lat1) * math.cos(math.radians(xCord[j])) * math.sin(lonDif/2) * math.sin(lonDif/2)

                finalDistance = radiusOfEarth * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                distances["cityi"] = i
                distances["cityj"] = j
                distances["distance"] = finalDistance
                distanceList.append(distances.copy())

                variables["cityi"] = i
                variables["cityj"] = j
                variables["pheromone"] = 1
                variables["visibility"] = 0
                variables["sumofpheromone"] = 0

                variablesList.append(variables.copy())

                j += 1
            i += 1
            j = i + 1

    bestTours = []
    bestTourLengths = []
    allTours = []
    while iterationNum <= numberOfIterations:
        antNumber = 0
        while antNumber <= numberOfAnts:
            first = True
            visited.clear()
            visitedLength = len(visited)
            while visitedLength < numberOfCities:
                if visitedLength == numberOfCities - 1:
                    lastCity = True
                if first:
                    firstCity = random.randint(0, numberOfCities - 1)
                    visited.append(firstCity)
                    currentCity = firstCity
                    first = False
                else:
                    currentCity = nextnode(currentCity, numberOfCities, visited, reductionRateOfPheromone,
                                           quantityOfPheromone, distanceList, alpha, beta, lastCity, firstCity)
                    visitedLength = len(visited)
                    visited.append(currentCity)

            lastCity = False
            antNumber += 1

            lengthOfTour.append(currentTour)
            currentTour = 0
            allTours.append(visited.copy())
            currentTourList.clear()
        minOfLengthOfTour = min(lengthOfTour)
        bestLength = minOfLengthOfTour
        bestTourLengths.append(bestLength)
        bestTours.append(allTours[lengthOfTour.index(minOfLengthOfTour)])
        print("Iteration #", iterationNum, "Complete ")
        lengthOfTour.clear()
        allTours.clear()
        iterationNum += 1
    minOfBestTourLength = min(bestTourLengths)
    print("Best found solution:", minOfBestTourLength)
    print("with path:", bestTours[bestTourLengths.index(minOfBestTourLength)])
