# Gray
'''
def doISODATAGray(image, K: int, TN: int, TS: float, TC:int, L: int, I: int) -> Image.Image:
    imgArray = numpy.array(image)
    imgX, imgY = numpy.shape(imgArray)
    clusterList = []
    # Generate K cluster centers randomly
    for i in range(0, K):
        randomX = random.randint(0, imgX - 1)
        randomY = random.randint(0, imgY - 1)
        duplicated = False
        for cluster in clusterList:
            if cluster.center == imgArray[randomX, randomY]:
                duplicated = True
                break
        if not duplicated:
            clusterList.append(Cluster(imgArray[randomX, randomY]))

    # Iteration
    iterationCount = 0
    didAnythingInLastIteration = True
    while True:
        iterationCount += 1

        # Clear the pixel lists of all clusters
        for cluster in clusterList:
            cluster.pixelList.clear()
        print("------")
        print("Iteration: {0}".format(iterationCount))

        # Classify all pixels into clusters
        print("Classifying...", end = '', flush = True)
        for row in range(0, imgX):
            for col in range(0, imgY):
                targetClusterIndex = 0
                targetClusterDistance = abs(int(imgArray[row, col]) - int(clusterList[0].center))
                # Classify
                for i in range(0, len(clusterList)):
                    currentDistance = abs(int(imgArray[row, col]) - int(clusterList[i].center))
                    if currentDistance < targetClusterDistance:
                        targetClusterDistance = currentDistance
                        targetClusterIndex = i
                clusterList[targetClusterIndex].pixelList.append(Pixel(row, col, imgArray[row, col]))
        print(" Finished.")

        # Check TN
        gotoNextIteration = False
        for i in range(len(clusterList) - 1, -1, -1):
            if len(clusterList[i].pixelList) < TN:
                # Re-classify
                clusterList.pop(i)
                gotoNextIteration = True
                break
        if gotoNextIteration:
            print("TN checking not passed.")
            continue
        print("TN checking passed.")

        # Recalculate the centers
        print("Recalculating the centers...", end = '', flush = True)
        for cluster in clusterList:
            sum = 0.0
            for pixel in cluster.pixelList:
                sum += int(pixel.color)
            ave = round(sum / len(cluster.pixelList))
            if ave != cluster.center:
                didAnythingInLastIteration = True
            cluster.center = ave
        print(" Finished.")
        if iterationCount > I:
            break
        if not didAnythingInLastIteration:
            print("More iteration is not necessary.")
            break

        # Calculate the average distance
        print("Preparing for Merging and Spliting...", end = '', flush = True)
        aveDisctanceList = []
        sumDistanceAll = 0
        for cluster in clusterList:
            currentSumDistance = 0
            for pixel in cluster.pixelList:
                currentSumDistance += abs(int(pixel.color) - int(cluster.center))
            aveDisctanceList.append(float(currentSumDistance) / len(cluster.pixelList))
            sumDistanceAll += currentSumDistance
        aveDistanceAll = float(sumDistanceAll) / (imgX * imgY)
        print(" Finished.")

        if (len(clusterList) <= K / 2) or not (iterationCount % 2 == 0 or len(clusterList) >= K * 2):
            # Split
            print("Split:", end = '', flush = True)
            beforeCount = len(clusterList)
            for i in range(len(clusterList) - 1, -1, -1):
                currentSD = 0.0
                for pixel in clusterList[i].pixelList:
                    currentSD += (int(pixel.color) - int(clusterList[i].center)) ** 2
                currentSD = math.sqrt(currentSD / len(clusterList[i].pixelList))
                if (currentSD > TS) and ((aveDisctanceList[i] > aveDistanceAll and len(clusterList[i].pixelList) > 2 * (TN + 1)) or (len(clusterList) < K / 2)):
                    gamma = 0.5 * currentSD
                    clusterList.append(Cluster(int(clusterList[i].center + gamma)))
                    clusterList.append(Cluster(int(clusterList[i].center - gamma)))
                    clusterList.pop(i)
            print(" {0} -> {1}".format(beforeCount, len(clusterList)))
        elif (iterationCount % 2 == 0) or (len(clusterList) >= K * 2) or (iterationCount == I):
            # Merge
            print("Merge:", end = '', flush = True)
            beforeCount = len(clusterList)
            didAnythingInLastIteration = False
            clusterPairList = []
            for i in range(0, len(clusterList)):
                for j in range(0, i):
                    currentDistance = abs(int(clusterList[i].center) - int(clusterList[j].center))
                    if currentDistance < TC:
                        clusterPairList.append(ClusterPair(i, j, currentDistance))

            clusterPairListSorted = sorted(clusterPairList, key = lambda clusterPair: clusterPair.distance)
            newClusterCenterList = []
            mergedClusterIndexList = []
            mergedPairCount = 0
            for clusterPair in clusterPairList:
                hasBeenMerged = False
                for index in mergedClusterIndexList:
                    if clusterPair.clusterAIndex == index or clusterPair.clusterBIndex == index:
                        hasBeenMerged = True
                        break
                if hasBeenMerged:
                    continue
                newCenter = int((len(clusterList[clusterPair.clusterAIndex].pixelList) * float(clusterList[clusterPair.clusterAIndex].center) + len(clusterList[clusterPair.clusterBIndex].pixelList) * float(clusterList[clusterPair.clusterBIndex].center)) / (len(clusterList[clusterPair.clusterAIndex].pixelList) + len(clusterList[clusterPair.clusterBIndex].pixelList)))
                newClusterCenterList.append(newCenter)
                mergedClusterIndexList.append(clusterPair.clusterAIndex)
                mergedClusterIndexList.append(clusterPair.clusterBIndex)
                mergedPairCount += 1
                if mergedPairCount > L:
                    break
            if len(mergedClusterIndexList) > 0:
                didAnythingInLastIteration = True
            mergedClusterIndexListSorted = sorted(mergedClusterIndexList, key = lambda clusterIndex: clusterIndex, reverse = True)
            for index in mergedClusterIndexListSorted:
                clusterList.pop(index)
            for center in newClusterCenterList:
                clusterList.append(Cluster(center))
            print(" {0} -> {1}".format(beforeCount, len(clusterList)))

    # Generate the new image martrix
    print("Over")
    print("Classified to {0} kinds.".format(len(clusterList)))
    newImgArray = numpy.zeros((imgX, imgY), dtype = numpy.uint8)
    for cluster in clusterList:
        for pixel in cluster.pixelList:
            newImgArray[pixel.x, pixel.y] = int(cluster.center)

    return Image.fromarray(newImgArray, mode = "L")
'''