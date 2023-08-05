#include <boost/python.hpp>
#include <boost/algorithm/string.hpp>
#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <cmath> 
#include <algorithm>
#include <tuple>

//TODO
//FIX DOUBLE DIGIT + NEGATITVE
//ADD SUPPORT MATERIAL
//FLOOR AND ROOF GEN

void runslice(std::string directory, int _posX, int _posY, int _speed, float _extrustion, float _infill, float _layerHeight) {
    std::cout << "Slicing File: " << directory << std::endl;
    int initPosition[2] = {_posX, _posY}; //X, Y 100 100
    float extrustionConst =  _extrustion; //1.0
    float infillConst = _infill; //1.0
    int speedConst = _speed; //1500
    float layerHeight = _layerHeight; //0.5

    std::ifstream infile(directory);
    std::string cube;

    int maxLayer = 0;
    std::vector<std::vector<int>> cubelist;
    std::vector<std::vector<int>> supportlist;
    //TODO FIX DOUBLE DIGIT AND NEGATIVE
    while(std::getline(infile, cube)){

        std::vector<std::string> tempVect;
        std::vector<int> cubevect;
        boost::split(tempVect, cube, boost::is_any_of(" "));

        for(int i = 0; i < 3; i++)
            cubevect.push_back(stoi(tempVect[i]));

        if(cube.back() != 's')
            cubelist.push_back(cubevect);
        else
            supportlist.push_back(cubevect);
            
        if(cubevect.at(2) > maxLayer)
                maxLayer = cubevect.at(2);
    }
    infile.close();

    //DETERMINE CUBE BLOCKS
    std::vector<std::vector<std::vector<int>>> cubeblocks(1, std::vector<std::vector<int>>(1, cubelist[0]));
    for(int cubeindex = 1; cubeindex < cubelist.size(); cubeindex++){
        std::vector<int> cube = cubelist.at(cubeindex);

        bool found = false;
        int mergeBlockIndex;

        for(int i = 0; i < cubeblocks.size(); i++){
            for(int j = 0; j < cubeblocks.at(i).size(); j++){
                if(cube.at(2) == cubeblocks.at(i).at(j).at(2) && ((std::abs(cube.at(0) - cubeblocks.at(i).at(j).at(0)) == 1 && cubeblocks.at(i).at(j).at(1) == cube.at(1)) || (std::abs(cube.at(1) - cubeblocks.at(i).at(j).at(1)) == 1 && cubeblocks.at(i).at(j).at(0) == cube.at(0)))){
                    if(!found){
                        cubeblocks[i].push_back(cube);
                        mergeBlockIndex = i;
                    }
                    else if(mergeBlockIndex != i){
                        for(int blockIndex = 0; blockIndex < cubeblocks[i].size(); blockIndex++)
                            cubeblocks[mergeBlockIndex].push_back(cubeblocks[i][blockIndex]);
                        cubeblocks.erase(cubeblocks.begin() + i);
                        break;
                    }
                    found = true;
                }
            }
        }

        if(!found)
            cubeblocks.push_back(std::vector<std::vector<int>>(1, cube));
    }
    
    std::vector<std::vector<std::string>> blockGcode;
    //GCODE GENERATION
    //GENERATE 2D ARRAY FOR EACH BLOCK
    for(int cubeBlockIndex = 0; cubeBlockIndex < cubeblocks.size(); cubeBlockIndex++){
        std::vector<std::vector<int>> cubeblock = cubeblocks.at(cubeBlockIndex);
        int maxX = cubeblock[0].at(0);
        int minX = cubeblock[0].at(0);
        int maxY = cubeblock[0].at(1);
        int minY = cubeblock[0].at(1);
    
        //GET MAX X AND Y IN CUBEBLOCK
        for(int i = 1; i < cubeblock.size(); i++){
            if(cubeblock[i].at(0) > maxX)
                maxX = cubeblock.at(i).at(0);
            if(cubeblock[i].at(0) < minX)
                minX = cubeblock.at(i).at(0);
            if(cubeblock[i].at(1) > maxY)
                maxY = cubeblock.at(i).at(1);
            if(cubeblock[i].at(1) < minY)
                minY = cubeblock.at(i).at(1);
        }

        //ADD CUBES TO 2D REPRESENTATION
        std::vector<std::vector<int>> printVect((maxY - minY + 1) * 10, std::vector<int> ((maxX - minX + 1) * 10, 0)); //2D representation of cubeblock

        for(int cubeIndex = 0; cubeIndex < cubeblock.size(); cubeIndex++){
            std::vector<int> cube = cubeblock.at(cubeIndex);
            //std::cout << "Cube " << cubeIndex << ": (" << cube.at(0) << ", " << cube.at(1) << ", " << cube.at(2) << ")" << std::endl;

            for(int i = 0; i < 10; i++){
                for(int j = 0; j < 10; j++){
                    //std::cout << "Writing to: " << (cube.at(1) -  minY - 1) * 10 + i << ", " << (cube.at(0) - minX) * 10 + j << std::endl;
                    printVect[(maxY - cube.at(1)) * 10 + i][(cube.at(0) - minX) * 10 + j] = 1;
                }
            }  
        }         

        //DETERMINE WALLS (DISGUSTING)
        for(int i = 0; i < (maxY - minY + 1) * 10; i++){
            for(int j = 0; j < (maxX - minX + 1) * 10; j++){
                if(printVect.at(i).at(j) == 1){
                    for(int x = -1; x <= 1; x++){ //CHECK INIDICES AROUND 3x3
                        if(x + j < (maxX - minX + 1) * 10 && x + j >= 0){
                            for(int y = -1; y <= 1; y++){
                                if(y + i < (maxY - minY + 1) * 10 && y + i >= 0){
                                    if(printVect.at(i + y).at(j + x) == 0)
                                        printVect[i][j] = 2;
                                }
                                else{
                                    printVect[i][j] = 2;
                                    break;
                                }
                            }
                        }
                        else{
                            printVect[i][j] = 2;
                            break;
                        }
                    }
                }
            }
        }

        //PRINT 2D ARRAY
        /*for(int i = 0; i < printVect.size(); i++){
            for(int j = 0; j < printVect[0].size(); j++){
                std::cout << printVect.at(i).at(j) << " ";
            }
            std::cout << std::endl;
        }*/

        //GENERATE GCODE FOR 2D SLICE
        std::vector<std::string> GCODE_SLICE_COMMANDS;

        //Find Starting Wall
        int startPos[2];
        for(int i = 0; i < printVect[0].size(); i++){
            if(printVect.at(0).at(i) == 2){
                startPos[0] = i;
                startPos[1] = printVect.size() - 1;
                break;
            }
        }
        //TRAVERSAL
        std::vector<std::string> gcode;

        gcode.push_back(";WALL BEGIN");
        gcode.push_back("G1 X" + std::to_string(initPosition[0] + startPos[0] + (minX * 10))  + " Y" + std::to_string(initPosition[1] + startPos[1] + (minY * 10) + 1) + " F" + std::to_string(speedConst));
        //WALLS
        int sliceStartPos[2] = {startPos[0] + 1, startPos[1]};
        int sliceEndPos[2] = {startPos[0] + 9, startPos[1]};
        int direction = 0; //R:0, D: 1, L: 2, U: 3
        int multi = 1;
        while(!(startPos[0] == sliceStartPos[0] && startPos[1] == sliceStartPos[1])){
            //CONVEX CORNERS
            if((direction == 0 && (sliceEndPos[0] + 1 == printVect[0].size() || printVect.at(printVect.size() - sliceEndPos[1] - 1).at(sliceEndPos[0] + 1) != 2)) ||
                (direction == 1 && (sliceEndPos[1] == 0 || printVect.at(printVect.size() - sliceEndPos[1]).at(sliceEndPos[0]) != 2)) ||
                (direction == 2 && (sliceEndPos[0] == 0 || printVect.at(printVect.size() - sliceEndPos[1] - 1).at(sliceEndPos[0] - 1) != 2)) ||
                (direction == 3 && (sliceEndPos[1] + 1 == printVect.size() || printVect.at(printVect.size() - sliceEndPos[1] - 2).at(sliceEndPos[0]) != 2))
                ){
                gcode.push_back("G1 X" + std::to_string((initPosition[0] + sliceEndPos[0] + (minX * 10) + 1) - ((initPosition[0] + sliceEndPos[0] + (minX * 10) + 1) % 10))  + " Y" + std::to_string((initPosition[1] + sliceEndPos[1] + (minY * 10) + 1) - ((initPosition[1] + sliceEndPos[1] + (minY * 10) + 1) % 10)) + " F" + std::to_string(speedConst) + " E" + std::to_string(multi * extrustionConst));
                sliceStartPos[0] = sliceEndPos[0];
                sliceStartPos[1] = sliceEndPos[1];

                if(direction == 3){ //RIGHT 
                    direction = 0;
                    sliceEndPos[0]--;
                }
                else if(direction == 0){ //DOWN
                    direction = 1;
                    sliceEndPos[1]++;
                }
                else if(direction == 1){ //LEFT
                    direction = 2;
                    sliceEndPos[0]++;
                }
                else if(direction == 2){ //UP
                    direction = 3;
                    sliceEndPos[1]--;
                }
                multi = 1;
            }
            //CONCAVE CORNERS
            else if((direction == 0 && printVect.at(printVect.size() - sliceEndPos[1] - 1).at(sliceEndPos[0] + 2) == 1) ||
                    (direction == 1 && printVect.at(printVect.size() - sliceEndPos[1] + 1).at(sliceEndPos[0]) == 1) ||
                    (direction == 2 && printVect.at(printVect.size() - sliceEndPos[1] - 1).at(sliceEndPos[0] - 2) == 1) ||
                    (direction == 3 && printVect.at(printVect.size() - sliceEndPos[1] - 3).at(sliceEndPos[0]) == 1)
            ){
                gcode.push_back("G1 X" + std::to_string((initPosition[0] + sliceEndPos[0] + (minX * 10) + 1) - ((initPosition[0] + sliceEndPos[0] + (minX * 10) + 1) % 10))  + " Y" + std::to_string((initPosition[1] + sliceEndPos[1] + (minY * 10) + 1) - ((initPosition[1] + sliceEndPos[1] + (minY * 10) + 1) % 10)) + " F" + std::to_string(speedConst) + " E" + std::to_string(multi * extrustionConst));
                sliceStartPos[0] = sliceEndPos[0];
                sliceStartPos[1] = sliceEndPos[1];
                if(direction == 1){ //RIGHT
                    direction = 0;
                    sliceEndPos[1]--;
                }
                else if(direction == 2){ //DOWN
                    direction = 1;
                    sliceEndPos[0]--;
                }
                else if(direction == 3){ //LEFT
                    direction = 2;
                    sliceEndPos[1]++;
                }
                else if(direction == 0){ //UP
                    direction = 3;
                    sliceEndPos[0]++;
                }
                multi = 1;
            }
            else{
                multi++;
            }
            if(direction == 0)
                sliceEndPos[0] += 10;
            else if(direction == 1)
                sliceEndPos[1] -= 10;
            else if(direction == 2)
                sliceEndPos[0] -= 10;
            else if(direction == 3)
                sliceEndPos[1] += 10;
        }
        gcode.push_back(";WALL END");

        //INFILL
        //FIND INFILL STARTING POINT
        int infillPos[2];
        for(int i = 0; i < printVect.size(); i++){
            if(printVect.at(i).at(0) == 2){
                infillPos[0] = 0;
                infillPos[1] = printVect.size() - i - 1;
                break;
            }
        }
        gcode.push_back(";INFILL BEGIN");
        gcode.push_back("G1 X" + std::to_string(initPosition[0] + infillPos[0] + (minX * 10))  + " Y" + std::to_string(initPosition[1] + infillPos[1] + (minY * 10) + 1) + " F1" + std::to_string(speedConst));

        //BEGIN INFILL
        bool down = true;
        for(float i = 0; i < printVect[0].size(); i += infillConst){
            int runningCount = 0;
            
            for(int j = (down ? 0 : printVect.size() - 1); down ? j < printVect.size() : j >= 0; down ? j++ : j--){ //down -> up
                if(printVect.at(j).at(i) != 0)
                    runningCount++;
                else if(runningCount != 0){
                    if(down)
                        gcode.push_back("G1 X" + std::to_string(initPosition[0] + i + (minX * 10)) + " Y" + std::to_string(initPosition[1] + printVect.size() - j + (minY * 10)) +  " F" + std::to_string(speedConst) + " E" + std::to_string((runningCount / 10) * extrustionConst));
                    else
                        gcode.push_back("G1 X" + std::to_string(initPosition[0] + i + (minX * 10)) + " Y" + std::to_string(initPosition[1] + printVect.size() - 1 - j + (minY * 10)) +  " F" + std::to_string(speedConst) + " E" + std::to_string((runningCount / 10) * extrustionConst));
                    runningCount = 0;
                }
            }
            if(runningCount != 0){
                if(down)
                    gcode.push_back("G1 X" + std::to_string(initPosition[0] + i + (minX * 10)) + " Y" + std::to_string(initPosition[1] + (minY * 10)) +  " F" + std::to_string(speedConst) + " E" + std::to_string((runningCount / 10) * extrustionConst));
                else
                    gcode.push_back("G1 X" + std::to_string(initPosition[0] + i + (minX * 10)) + " Y" + std::to_string(initPosition[1] + printVect.size() + (minY * 10)) +  " F" + std::to_string(speedConst) + " E" + std::to_string((runningCount / 10) * extrustionConst));
            }
            if(i < printVect[0].size() - infillConst)
                gcode.push_back("G1 X" + std::to_string(initPosition[0] + i + infillConst + (minX * 10)) + " F" + std::to_string(speedConst));
            down = !down;
        }
        gcode.push_back(";INFILL END");

        blockGcode.push_back(gcode);
    }
    //WRITE TO GCODE FILE

    std::ofstream gcode;
    gcode.open (directory.erase(directory.length() - 6).append(".gcode"));

    gcode << "M190 S70" << std::endl;
    gcode << "M109 S205" << std::endl;
    gcode << "G28" << std::endl;
    gcode << "G92 E0" << std::endl;
    gcode << "G1 Z4 F3000" << std::endl;
    gcode << "M83" << std::endl;

    //Can be improved
    for(float z = layerHeight; z <= ((maxLayer + 1) * 10); z += layerHeight){
        gcode << "G1 Z" << z << std::endl;

        for(int i = 0; i < cubeblocks.size(); i++){
            if((std::fmod(z, 10.0f) == 0.0f && cubeblocks.at(i).at(0).at(2) == ((int)z / 10) - 1) || (std::fmod(z, 10.0f) != 0.0f && cubeblocks.at(i).at(0).at(2) == ((int)z - (int)z % 10) / 10)){
                for(int j = 0; j < blockGcode[i].size(); j++){
                    gcode << blockGcode[i][j] << std::endl;
                }
            }
        }
        for(int i = 0; i < supportlist.size(); i++){
            if((std::fmod(z, 10.0f) == 0.0f && supportlist.at(i).at(2) == ((int)z / 10) - 1) || (std::fmod(z, 10.0f) != 0.0f && supportlist.at(i).at(2) == ((int)z - (int)z % 10) / 10)){
                gcode << ";SUPPORT BEGIN" << std::endl;
                gcode << "G1 X" << initPosition[0] + supportlist.at(i).at(0) * 10 + 1  << " Y" << initPosition[1] + supportlist.at(i).at(1) * 10 + 1<< " F" << speedConst << std::endl;
                gcode << "G1 X" << initPosition[0] + supportlist.at(i).at(0) * 10 + 9 << " Y" << initPosition[1] + supportlist.at(i).at(1) * 10 + 9 << " F" << speedConst << " E" << extrustionConst * 1.3 << std::endl;
                gcode << "G1 X" << initPosition[0] + supportlist.at(i).at(0) * 10 + 9 << " Y" << initPosition[1] + supportlist.at(i).at(1) * 10 + 1<< " F" <<speedConst << std::endl;
                gcode << "G1 X" << initPosition[0] + supportlist.at(i).at(0) * 10 + 1<< " Y" << initPosition[1] + supportlist.at(i).at(1) * 10 + 9 << " F" << speedConst << " E" << extrustionConst * 1.3 << std::endl;
                gcode << ";SUPPORT END" << std::endl;
            }
        }
    }
    
    gcode << "G1 Z" << ((maxLayer + 1) * 10) + 5 << std::endl;
    gcode.close();

    std::cout << "Slice Finished" << std::endl;
}

BOOST_PYTHON_MODULE(_slice) {
    using namespace boost::python;

    def("runslice", runslice);
}