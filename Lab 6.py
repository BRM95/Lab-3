from collections import defaultdict
import csv
import sys
import re
import unittest
import random

switch = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,float('inf')]#A global array, containing the possible switching times upto 4 with a possibility of a machine breaking, being assigned infinity
breakCheck = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,float('inf')]#Check if the current station is broken or not (1/15 possibility of infinity)


def random1(n,l1,l2,l3): #Assigns random values to the three stations/lanes
    i = 0;
    while i <= n: #Random integers less than n are assigned to our three lanes;
        l1.append(random.randint(1, n));#These will be the station costs (will always be less than or equal to the number of stations)
        l2.append(random.randint(1, n));# 'N' represents the total number of stations
        l3.append(random.randint(1, n));
        i+=1;
    l1.append('l1');#The element after the last station will be the name of the lane.
    l2.append('l2');
    l3.append('l3');
    return l1;

def recursive1(n,l1,l2,l3,sol,sol1,sol2):#Recursive solution without memoization      
    #print "n ",n, "len(sol) ",len(sol)
    if n == 0:#If we have recursed back to 0, select the minimum from solution
        if l1[0]<l2[0] and l1[0]<l3[0]:
            sol.append(('l1',l1[0]));
            temp = checkLesser(l2,l3,0,0,0,0);
            sol1.append(temp[0]);sol2.append(temp[1])
            sol1 = list(set(sol1));sol2 = list(set(sol2))            
        else:
            if l2[0]<l1[0] and l2[0]<l3[0]:
                sol.append(('l2',l2[0]));
                temp = checkLesser(l1,l3,0,0,0,0);
                sol1.append(temp[0]);sol2.append(temp[1])
                sol1 = list(set(sol1));sol2 = list(set(sol2))                
            else:
                sol.append(('l3',l3[0]));                
                temp = checkLesser(l1,l2,0,0,0,0);
                sol1.append(temp[0]);sol2.append(temp[1])
                sol1 = list(set(sol1));sol2 = list(set(sol2))                
        return sol;
                    
    else:
        sol= recursive1(n-1,l1,l2,l3,sol,sol1,sol2);
        switch1 =  random.choice(switch); switch2 = random.choice(switch); switch3 = random.choice(switch);
        broken = random.choice(breakCheck); #Contains the possibility of a station being broken or not   
        if(sol == 'l1'):#Checking if the previous station was L1
            if sol[n-1][1] + l1[n] + broken < sol[n-1][1] + l2[n] + switch2 and sol[n-1][1] + l1[n] < sol[n-1][1] + l3[n] + switch3: #4 is assumed to be the cost of switching between stations
                sol = list(recursive1(n-1,l1,l2,l3,sol,sol1,sol2));
                sol.append(('l1',(l1[n]+sol[n-1][1])));
                temp = checkLesser(l2,l3,switch2,switch3,sol[n-1][1],n);
                sol1.append(temp[0]);sol2.append(temp[1])                
                sol1 = list(set(sol1));sol2 = list(set(sol2))
            else:
                if sol[n-1][1] + l2[n] + switch2 < sol[n-1][1] + l1[n] + broken and sol[n-1][1] + l2[n] + switch2 < sol[n-1][1] + l3[n] + switch3: #4 is assumed to be the cost of switching between stations
                    sol = list(recursive1(n-1,l1,l2,l3,sol,sol1,sol2));
                    sol.append(('l2',(l2[n] + sol[n-1][1] + switch2)));
                    temp = checkLesser(l1,l3,broken,switch3,sol[n-1][1],n);
                    sol1.append(temp[0]);sol2.append(temp[1])
                    sol1= list(set(sol1));sol2= list(set(sol2))
                else:
                    sol = list(recursive1(n-1,l1,l2,l3,sol,sol1,sol2));
                    sol.append(('l3',(l3[n] + sol[n-1][1] + switch3)));
                    temp = checkLesser(l1,l2,broken,switch2,sol[n-1][1],n);
                    sol1.append(temp[0]);sol2.append(temp[1])
                    sol1= list(set(sol1));sol2= list(set(sol2))
        else:
            if(sol[n-1][0] == 'l2'):#Checking if the previous station was L2
                if sol[n-1][1] + l2[n] + broken < sol[n-1][1] + l1[n] + switch1 and sol[n-1][1] + l2[n] + broken < sol[n-1][1] + l3[n] + switch3: #4 is assumed to be the cost of switching between stations
                    sol = list(recursive1(n-1,l1,l2,l3,sol,sol1,sol2));
                    sol.append(('l2',(l2[n]+sol[n-1][1])));
                    temp = checkLesser(l1,l3,switch1,switch3,sol[n-1][1],n);
                    sol1.append(temp[0]);sol2.append(temp[1])
                    sol1= list(set(sol1));sol2= list(set(sol2))
                else:
                    if sol[n-1][1] + l1[n] + switch1 < sol[n-1][1] + l2[n] + broken and sol[n-1][1] + l1[n] + switch1 < sol[n-1][1] + l3[n] + switch3: #4 is assumed to be the cost of switching between stations
                        sol = list(recursive1(n-1,l1,l2,l3,sol,sol1,sol2));
                        sol.append(('l1',(l1[n] + sol[n-1][1] + switch1)));
                        temp = checkLesser(l2,l3,broken,switch3,sol[n-1][1],n);
                        sol1.append(temp[0]);sol2.append(temp[1])
                        sol1= list(set(sol1));sol2= list(set(sol2))
                    else:
                        sol = list(recursive1(n-1,l1,l2,l3,sol,sol1,sol2));
                        sol.append(('l3',(l3[n] + sol[n-1][1] + switch3)));
                        temp = checkLesser(l1,l2,switch1,broken,sol[n-1][1],n);
                        sol1.append(temp[0]);sol2.append(temp[1])
                        sol1= list(set(sol1));sol2= list(set(sol2))
            else: #Otherwise, the station is L3
                if sol[n-1][1] + l3[n] + broken < sol[n-1][1] + l2[n] + switch2 and sol[n-1][1] + l3[n] + broken < sol[n-1][1] + l1[n] + switch1: 
                    sol = list(recursive1(n-1,l1,l2,l3,sol,sol1,sol2));
                    sol.append(('l3',(l3[n]+sol[n-1][1])));
                    temp = checkLesser(l1,l2,switch1,switch2,sol[n-1][1],n);
                    sol1.append(temp[0]);sol2.append(temp[1])                    
                    sol1= list(set(sol1));sol2= list(set(sol2))
                else:
                    if sol[n-1][1] + l1[n] + switch1 < sol[n-1][1] + l3[n] + broken and sol[n-1][1] + l1[n] + switch1 < sol[n-1][1] + l2[n] + switch2: 
                        sol = list(recursive1(n-1,l1,l2,l3,sol,sol1,sol2));
                        sol.append(('l1',(l1[n] + sol[n-1][1] + switch1)));
                        temp = checkLesser(l3,l2,broken,switch2,sol[n-1][1],n);
                        sol1.append(temp[0]);sol2.append(temp[1])
                        sol1= list(set(sol1));sol2= list(set(sol2))
                    else:
                        sol = list(recursive1(n-1,l1,l2,l3,sol,sol1,sol2));
                        sol.append(('l2',(l2[n] + sol[n-1][1] + switch2)));
                        temp = checkLesser(l3,l1,broken,switch1,sol[n-1][1],n);
                        sol1.append(temp[0]);sol2.append(temp[1])                        
                        sol1= list(set(sol1));sol2= list(set(sol2))

        return sol;   

def checkLesser(l1,l2,switch1,switch2,pathCost,n):#Path cost here is the cost required to get to this particular station i.e. sol[n-1][1]
    temp = []
    if pathCost + l1[n] + switch1 < pathCost + l2[n] + switch2:
        temp.append((l1[-1],(pathCost + l1[n] + switch1)));
        temp.append((l2[-1],(pathCost + l2[n] + switch2)));

    else:
        temp.append((l2[-1],(pathCost + l2[n] + switch2)));
        temp.append((l1[-1],(pathCost + l1[n] + switch1)));
    return temp        
    
def recursive2(n,l1,l2,l3,sol,sol1,sol2):#Recursive solution with memoization      
    #print "n ",n, "len(sol) ",len(sol)
    if n == 0:#If we have recursed back to 0, select the minimum from solution
        if l1[0]<l2[0] and l1[0]<l3[0]:
            sol.append(('l1',l1[0]));
            temp = checkLesser(l2,l3,0,0,0,0);
            sol1.append(temp[0]);sol2.append(temp[1])
        else:
            if l2[0]<l1[0] and l2[0]<l3[0]:                
                sol.append(('l2',l2[0]));
                temp = checkLesser(l1,l3,0,0,0,0);
                sol1.append(temp[0]);sol2.append(temp[1])
            else:
                sol.append(('l3',l3[0]));                
                temp = checkLesser(l1,l2,0,0,0,0);
                sol1.append(temp[0]);sol2.append(temp[1])                
        return sol;
                    
    else:
        recursive2(n-1,l1,l2,l3,sol,sol1,sol2);
        switch1 =  random.choice(switch); switch2 = random.choice(switch); switch3 = random.choice(switch);
        broken = random.choice(breakCheck); #Contains the possibility of a station being broken or not   
        if len(sol) == n and sol:
            if(sol[n-1][0] == 'l1'):#Checking if the previous station was L1
                if sol[n-1][1] + l1[n] + broken < sol[n-1][1] + l2[n] + switch2 and sol[n-1][1] + l1[n] < sol[n-1][1] + l3[n] + switch3: #4 is assumed to be the cost of switching between stations
                    sol.append(('l1',(l1[n]+sol[n-1][1])));
                    temp = checkLesser(l2,l3,switch2,switch3,sol[n-1][1],n);
                    sol1.append(temp[0]);sol2.append(temp[1])                
                else:
                    if sol[n-1][1] + l2[n] + switch2 < sol[n-1][1] + l1[n] + broken and sol[n-1][1] + l2[n] + switch2 < sol[n-1][1] + l3[n] + switch3: #4 is assumed to be the cost of switching between stations
                        sol.append(('l2',(l2[n] + sol[n-1][1] + switch2)));
                        temp = checkLesser(l1,l3,broken,switch3,sol[n-1][1],n);
                        sol1.append(temp[0]);sol2.append(temp[1])                
                    else:
                        sol.append(('l3',(l3[n] + sol[n-1][1] + switch3)));
                        temp = checkLesser(l1,l2,broken,switch2,sol[n-1][1],n);
                        sol1.append(temp[0]);sol2.append(temp[1])                
            else:
                if(sol[n-1][0] == 'l2'):#Checking if the previous station was L2
                    if sol[n-1][1] + l2[n] + broken < sol[n-1][1] + l1[n] + switch1 and sol[n-1][1] + l2[n] + broken < sol[n-1][1] + l3[n] + switch3: #4 is assumed to be the cost of switching between stations
                        sol.append(('l2',(l2[n]+sol[n-1][1])));
                        temp = checkLesser(l1,l3,switch1,switch3,sol[n-1][1],n);
                        sol1.append(temp[0]);sol2.append(temp[1])                
                    else:
                        if sol[n-1][1] + l1[n] + switch1 < sol[n-1][1] + l2[n] + broken and sol[n-1][1] + l1[n] + switch1 < sol[n-1][1] + l3[n] + switch3: #4 is assumed to be the cost of switching between stations
                            sol.append(('l1',(l1[n] + sol[n-1][1] + switch1)));
                            temp = checkLesser(l2,l3,broken,switch3,sol[n-1][1],n);
                            sol1.append(temp[0]);sol2.append(temp[1])                
                        else:
                            sol.append(('l3',(l3[n] + sol[n-1][1] + switch3)));
                            temp = checkLesser(l1,l2,switch1,broken,sol[n-1][1],n);
                            sol1.append(temp[0]);sol2.append(temp[1])                
                else: #Otherwise, the station is L3
                    if sol[n-1][1] + l3[n] + broken < sol[n-1][1] + l2[n] + switch2 and sol[n-1][1] + l3[n] + broken < sol[n-1][1] + l1[n] + switch1: 
                        sol.append(('l3',(l3[n]+sol[n-1][1])));
                        temp = checkLesser(l1,l2,switch1,switch2,sol[n-1][1],n);
                        sol1.append(temp[0]);sol2.append(temp[1])                
                    else:
                        if sol[n-1][1] + l1[n] + switch1 < sol[n-1][1] + l3[n] + broken and sol[n-1][1] + l1[n] + switch1 < sol[n-1][1] + l2[n] + switch2: 
                            sol.append(('l1',(l1[n] + sol[n-1][1] + switch1)));
                            temp = checkLesser(l3,l2,broken,switch2,sol[n-1][1],n);
                            sol1.append(temp[0]);sol2.append(temp[1])                
                        else:
                            sol.append(('l2',(l2[n] + sol[n-1][1] + switch2)));
                            temp = checkLesser(l3,l1,broken,switch1,sol[n-1][1],n);
                            sol1.append(temp[0]);sol2.append(temp[1])                
            return sol;


def iterative(n,l1,l2,l3,sol,sol1,sol2): #iterative solution with memoization
    i = 0; 
    while i <= n: #This is the essence of an iterative solution, with the loop iterating till n, i.e. the number of stations
        switch1 =  random.choice(switch); switch2 = random.choice(switch); switch3 = random.choice(switch);
        broken = random.choice(breakCheck); #Contains the possibility of a station being broken or not (The main station); 
        if i ==  0:
            if l1[0]<l2[0] and l1[0]<l3[0]:
                sol.append(('l1',l1[0]));
                temp = checkLesser(l2,l3,0,0,0,0);
                sol1.append(temp[0]);sol2.append(temp[1])            
            else:
                if l2[0]<l1[0] and l2[0]<l3[0]:
                    sol.append(('l2',l2[0]));
                    temp = checkLesser(l1,l3,0,0,0,0);
                    sol1.append(temp[0]);sol2.append(temp[1])
                else:
                    sol.append(('l3',l3[0]));
                    temp = checkLesser(l1,l2,0,0,0,0);
                    sol1.append(temp[0]);sol2.append(temp[1])  
        else:
            if(sol[i-1][0] == 'l1'):#Checking if the previous station was L1            
                if sol[i-1][1] + l1[i] + broken < sol[i-1][1] + l2[i] + switch2 and sol[i-1][1] + l1[i] < sol[i-1][1] + l3[i] + switch3: #4 is assumed to be the cost of switching between stations
                    sol.append(('l1',(l1[i]+sol[i-1][1])));
                    temp = checkLesser(l2,l3,switch2,switch3,sol[i-1][1],i);
                    sol1.append(temp[0]);sol2.append(temp[1])  
                else:
                    if sol[i-1][1] + l2[i] + switch2 < sol[i-1][1] + l1[i] + broken and sol[i-1][1] + l2[i] + switch2 < sol[i-1][1] + l3[i] + switch3: #4 is assumed to be the cost of switching between stations
                        sol.append(('l2',(l2[i] + sol[i-1][1] + switch2)));
                        temp = checkLesser(l1,l3,broken,switch3,sol[i-1][1],i);
                        sol1.append(temp[0]);sol2.append(temp[1]) 
                    else:
                        sol.append(('l3',(l3[i] + sol[i-1][1] + switch3)));
                        temp = checkLesser(l1,l2,broken,switch2,sol[i-1][1],i);
                        sol1.append(temp[0]);sol2.append(temp[1]);    
            else:
                if(sol[i-1][0] == 'l2'):#Checking if the previous station was L2
                    if sol[i-1][1] + l2[i] + broken < sol[i-1][1] + l1[i] + switch1 and sol[i-1][1] + l2[i] + broken < sol[i-1][1] + l3[i] + switch3: #4 is assumed to be the cost of switching between stations
                        sol.append(('l2',(l2[i]+sol[i-1][1])));
                        temp = checkLesser(l1,l3,switch1,switch3,sol[i-1][1],i);
                        sol1.append(temp[0]);sol2.append(temp[1])    
                    else:
                        if sol[i-1][1] + l1[i] + switch1 < sol[i-1][1] + l2[i] + broken and sol[i-1][1] + l1[i] + switch1 < sol[i-1][1] + l3[i] + switch3: #4 is assumed to be the cost of switching between stations
                            sol.append(('l1',(l1[i] + sol[i-1][1] + switch1)));
                            temp = checkLesser(l2,l3,broken,switch3,sol[i-1][1],i);
                            sol1.append(temp[0]);sol2.append(temp[1])      
                        else:
                            sol.append(('l3',(l3[i] + sol[i-1][1] + switch3)));
                            temp = checkLesser(l1,l2,switch1,broken,sol[i-1][1],i);
                            sol1.append(temp[0]);sol2.append(temp[1]) 
                else: #Otherwise, the station is L3
                    if sol[i-1][1] + l3[i] + broken < sol[i-1][1] + l2[i] + switch2 and sol[i-1][1] + l3[i] + broken < sol[i-1][1] + l1[i] + switch1: #4 is assumed to be the cost of switching between stations
                        sol.append(('l3',(l3[i]+sol[i-1][1])));
                        temp = checkLesser(l1,l2,switch1,switch2,sol[i-1][1],i);
                        sol1.append(temp[0]);sol2.append(temp[1]) 
                    else:
                        if sol[i-1][1] + l1[i] + switch1 < sol[i-1][1] + l3[i] + broken and sol[i-1][1] + l1[i] + switch1 < sol[i-1][1] + l2[i] + switch2: #4 is assumed to be the cost of switching between stations
                            sol.append(('l1',(l1[i] + sol[i-1][1] + switch1)));
                            temp = checkLesser(l3,l2,broken,switch2,sol[i-1][1],i);
                            sol1.append(temp[0]);sol2.append(temp[1])  
                        else:
                            sol.append(('l2',(l2[i] + sol[i-1][1] + switch2)));  
                            temp = checkLesser(l3,l1,broken,switch1,sol[i-1][1],i);
                            sol1.append(temp[0]);sol2.append(temp[1])                
        i+=1
    return sol;


def main():#The main function, used to create the lanes and subsequently compute costs
    var = int(raw_input("Please enter lane length \n(The lane will have +1 stations of entered value): "));#Taking user input
    l1 = []; l2 = []; l3= []; #Our three lanes are lists
    sol = []; sol1 = []; sol2 = [];
    solI=[]; sol1I = []; sol2I = []; #Holds the iterative solution
    solR=[]; sol1R = []; sol2R = []; #Holds the iterative solution
    random1(var,l1,l2,l3);
    #print l1, " 2nd ", l2, " 3rd ",l3
    recursive2(var,l1,l2,l3,sol,sol1,sol2);
    print "Computer #1: ",sol,"\n\nComputer #2: ",sol1,"\n\nComputer #3: ",sol2
    iterative(var,l1,l2,l3,solI,sol1I,sol2I);
    print "\nComputerI #1: ",solI,"\n\nComputerI #2: ",sol1I,"\n\nComputerI #3: ",sol2I
    recursive1(var,l1,l2,l3,solR,sol1R,sol2R);
    print "\nComputerR #1: ",solR," ",set(sol1R)," ",set(sol2R)    
    
class cpuSimulator(unittest.TestCase):

    def testOne(self): #TestOne checks if the random function is working correctly
      self.assertEquals(6,len(random1(4,[],[],[])))#Here we check if the size of the returned array is what we expect.

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(cpuSimulator)#Code to automatically execute a unit test at startup
    unittest.TextTestRunner(verbosity=2).run(suite)
    main()
                 
        
