import numpy as np
import time
import copy 

class MeasureTime:

    def __init__(self,tag="It"):
        self.tag=tag

    def __enter__(self):
        self.t0=time.time()

    def __exit__(self,type,value,traceback):
        print(f"\n{self.tag} took {time.time()-self.t0} s.\n")

def read_puzzle(text,n=9):

    return np.array([int(num) for num in text],dtype=int).reshape((n,n))


def get_block_inds(rowind,colind,m):
    return rowind//m*m+colind//m
    

def baby_sudoku(puzzle0,n=3):
    numset={*range(1,n+1)}
    row_opts=[set()]*n
    col_opts=[set()]*n
    for ind in range(n):
        row=puzzle0[ind,:]
        col=puzzle0[:,ind]
        if len(row[row>0])!=len(set(row[row>0])) or len(col[col>0])!=len(set(col[col>0])):
            return False,None
            
    def _solve(puzzle):
        zero_inds=list(zip(*np.where(puzzle==0)))

        if not zero_inds:
            return True,puzzle
        for ind in range(n):
            row_opts[ind]=numset.difference(puzzle[ind,:])
            col_opts[ind]=numset.difference(puzzle[:,ind])

        for (rowind,colind) in zero_inds:
            options=row_opts[rowind].intersection(col_opts[colind])
            if not options:
                return False,None
            for num in options:
                #print("bf",rowind,colind,num)
                puzzle[rowind,colind]=num
                success,result=_solve(puzzle)
                #print("af",rowind,colind,num,success)
                if success:
                    return True,puzzle
        return False,None
                
        
def sudoku(puzzle0,n=9):
    numset={*range(1,n+1)}
    row_opts=[set()]*n
    col_opts=[set()]*n

    m=int(np.sqrt(n))
    block_opts=[set()]*n
    blockinds=np.array([[get_block_inds(i,j,m) for j in range(n)] for i in range(n)])
    #print("puzzle:",puzzle0)#;#input()

    for ind in range(n):
        row=puzzle0[ind,:]
        col=puzzle0[:,ind]
        if len(row[row>0])!=len(set(row[row>0])) or len(col[col>0])!=len(set(col[col>0])):
            #print("Spatne zadane")
            return False,None
        zero_inds=list(zip(*np.where(puzzle0==0)))    
    def _solve(puzzle,zer_num=0):
        

        if zer_num>=len(zero_inds):
            return True,puzzle
        for ind in range(n):
            row_opts[ind]=numset.difference(puzzle[ind,:])
            col_opts[ind]=numset.difference(puzzle[:,ind])
            block_row=ind//m
            block_col=ind%m
            block_opts[ind]=numset.difference(puzzle[block_row*m:(block_row+1)*m,block_col*m:(block_col+1)*m].reshape(m*m))
        
        (rowind,colind)=zero_inds[zer_num]
            
        options=row_opts[rowind].intersection(col_opts[colind]).intersection(block_opts[blockinds[rowind,colind]])
        if len(zero_inds)==1 and len(options)>1:
            raise ValueError("Non-unique!")
        if not options:
            #print(f"No options!({rowind+1},{colind+1})\n",puzzle)
            #input()
            return False,None
        for num in options:
            #print(f"In ({rowind+1},{colind+1}),options: {options},trying: {num}")
            
            puzzle[rowind,colind]=num
            #print(puzzle);#input()
            success,result=_solve(np.array(puzzle),zer_num+1)
            if success:
                return True,result
            #print(f"In ({rowind+1},{colind+1}),options: {options},failed: {num}")
            #input()
        return False,None

    return _solve(puzzle0)

def sudoku2(puzzle0,n=9):
    global failed_count
    numset={*range(1,n+1)}
    row_opts=[set()]*n
    col_opts=[set()]*n

    m=int(np.sqrt(n))
    block_opts=[set()]*n
    blockinds=np.array([[get_block_inds(i,j,m) for j in range(n)] for i in range(n)])
    failed_count=0
    #print("puzzle:",puzzle0)#;#input()

    for ind in range(n):
        row=puzzle0[ind,:]
        col=puzzle0[:,ind]
        if len(row[row>0])!=len(set(row[row>0])) or len(col[col>0])!=len(set(col[col>0])):
            #print("Spatne zadane")
            return False,None
        
        for ind in range(n):
            row_opts[ind]=numset.difference(puzzle[ind,:])
            col_opts[ind]=numset.difference(puzzle[:,ind])
            block_row=ind//m
            block_col=ind%m
            block_opts[ind]=numset.difference(puzzle[block_row*m:(block_row+1)*m,block_col*m:(block_col+1)*m].reshape(m*m))
        zero_inds=sorted(zip(*np.where(puzzle0==0)),key=lambda inds: (row_opts[inds[0]].intersection(col_opts[inds[1]]).intersection(block_opts[blockinds[inds[0],inds[1]]])))    

    def _solve(puzzle,zer_num=0):
        global failed_count

        if zer_num>=len(zero_inds):
            return True,puzzle
        for ind in range(n):
            row_opts[ind]=numset.difference(puzzle[ind,:])
            col_opts[ind]=numset.difference(puzzle[:,ind])
            block_row=ind//m
            block_col=ind%m
            block_opts[ind]=numset.difference(puzzle[block_row*m:(block_row+1)*m,block_col*m:(block_col+1)*m].reshape(m*m))
        
        (rowind,colind)=zero_inds[zer_num]
            
        options=row_opts[rowind].intersection(col_opts[colind]).intersection(block_opts[blockinds[rowind,colind]])
        #if len(zero_inds)==1 and len(options)>1:
        #    raise ValueError("Non-unique!")
        if not options:
            #print(f"No options!({rowind+1},{colind+1})\n",puzzle)
            #input()
            failed_count+=1
            return False,None
        for num in options:
            #print(f"In ({rowind+1},{colind+1}),options: {options},trying: {num}")
            
            puzzle[rowind,colind]=num
            #print(puzzle);#input()
            success,result=_solve(np.array(puzzle),zer_num+1)
            if success:
                return True,result
            #print(f"In ({rowind+1},{colind+1}),options: {options},failed: {num}")
            #input()
        return False,None

    sol=_solve(np.array(puzzle0))
    print("Number of attempts: ",failed_count+1)
    return sol

def sudoku3(puzzle0,n=9):
    global failed_count
    numset={*range(1,n+1)}
    row_opts=[set()]*n
    col_opts=[set()]*n

    m=int(np.sqrt(n))
    block_opts=[set()]*n
    blockinds=np.array([[get_block_inds(i,j,m) for j in range(n)] for i in range(n)])
    failed_count=0
    #print("puzzle:",puzzle0)#;#input()

    for ind in range(n):
        row=puzzle0[ind,:]
        col=puzzle0[:,ind]
        if len(row[row>0])!=len(set(row[row>0])) or len(col[col>0])!=len(set(col[col>0])):
            #print("Spatne zadane")
            return False,None
        
        for ind in range(n):
            row_opts[ind]=numset.difference(puzzle[ind,:])
            col_opts[ind]=numset.difference(puzzle[:,ind])
            block_row=ind//m
            block_col=ind%m
            block_opts[ind]=numset.difference(puzzle[block_row*m:(block_row+1)*m,block_col*m:(block_col+1)*m].reshape(m*m))
        zero_inds=list(zip(*np.where(puzzle0==0)))
        zero_inds=[(zero_ind[0],zero_ind[1],blockinds[zero_ind[0],zero_ind[1]]) for zero_ind in zero_inds]
        print(zero_inds)
        ind_queue=[[zero_ind,len(row_opts[zero_ind[0]].intersection(col_opts[zero_ind[1]]).intersection(block_opts[zero_ind[2]]))] for zero_ind in zero_inds]
        ind_queue=sorted(ind_queue,key=lambda x: x[1])
  

    def _solve(puzzle,ind_queue,row_opts,col_opts,block_opts,zer_num=0):
        global failed_count

        if zer_num>=len(zero_inds):
            return True,puzzle
      
        
        (rowind,colind,blockind)=ind_queue[0][0]
            
        options=row_opts[rowind].intersection(col_opts[colind]).intersection(block_opts[blockind])
        #if len(zero_inds)==1 and len(options)>1:
        #    raise ValueError("Non-unique!")
        if not options:
            #print(f"No options!({rowind+1},{colind+1})\n",puzzle)
            #input()
            failed_count+=1
            return False,None
        for num in options:
            #print(f"In ({rowind+1},{colind+1}),options: {options},trying: {num}")
            
            puzzle[rowind,colind]=num
            #print(puzzle);#input()
            new_queue=copy.deepcopy(ind_queue[1:])
            nrow_opts=copy.deepcopy(row_opts)
            ncol_opts=copy.deepcopy(col_opts)
            nblock_opts=copy.deepcopy(block_opts)
            nrow_opts[rowind].remove(num)
            ncol_opts[colind].remove(num)
            nblock_opts[blockind].remove(num)
            for ind,((rowind2,colind2,blockind2),_) in enumerate(new_queue):
                if rowind2==rowind or colind2==colind or blockind2==blockind:
        
                    new_queue[ind][1]-=1
            new_queue=sorted(new_queue,key=lambda x: x[1])

            success,result=_solve(np.array(puzzle),new_queue,nrow_opts,ncol_opts,nblock_opts,zer_num+1)
            if success:
                return True,result
            #print(f"In ({rowind+1},{colind+1}),options: {options},failed: {num}")
            #input()
        return False,None

    sol=_solve(np.array(puzzle0),ind_queue,row_opts,col_opts,block_opts)
    print("Number of attempts: ",failed_count+1)
    return sol
#puzzle=read_puzzle("004006079000000602056092300078061030509000406020540890007410920105000000840600100",n=9)
#puzzle=read_puzzle("196305482427018356053204079612740835948501000075082041500026790789150260064897510",n=9)
#puzzle=read_puzzle("400000805030000000000700000020000060000080400000010000000603070500200000104000000",n=9)
puzzle=read_puzzle("020503001050000349070190056000000700730200508005074130008309000302006900197052603",n=9)
#puzzle=read_puzzle("070000043040009610800634900094052000358460020000800530080070091902100005007040802",n=9)
#puzzle=read_puzzle("004300209005009001070060043006002087190007400050083000600000105003508690042910300",n=9)
#s="078010609203009008410060052720106030000400700091305000932000400005720010000008006"
#puzzle=read_puzzle(s,n=9)
#puzzle0=read_puzzle("231002023",n=3)
#def solve_sudoku(puzzle):
#    def _solve()
##print(baby_sudoku(puzzle0,n=3))
with MeasureTime("Solving the sudoku"):
    solvable,solution=sudoku2(puzzle,n=9)
    n=9
    from colorama import Fore,Style

    if solvable:
        print("\n{:^30}".format("Puzzle:")+"\t\t\t"+"{:^35}".format("Solution:")+"\n")
        for row in range(n//2):
            for col_sep in range(n//3):
                print(f"{Fore.RED}|{Fore.BLACK} "+" | ".join((str(num) if num>0 else " " for num in puzzle[row,col_sep*n//3:(col_sep+1)*n//3])),end="")
            print(f"{Fore.RED} |{Fore.BLACK}",end="")
            print("\t\t",end="")
            for col_sep in range(n//3):
                print(f"{Fore.RED}|{Fore.BLACK} "+" | ".join((str(num) if num>0 else " " for num in solution[row,col_sep*n//3:(col_sep+1)*n//3])),end="")
            print(f"{Fore.RED} |{Fore.BLACK}")
            if (row+1)%3==0:
                print("  "*(n)+"\t\t"+"  "*(n))
        for col_sep in range(n//3):
            print(f"{Fore.RED}|{Fore.BLACK} "+" | ".join((str(num) if num>0 else " " for num in puzzle[n//2,col_sep*n//3:(col_sep+1)*n//3])),end="")
        print(f"{Fore.RED} |{Fore.BLACK}",end="")
        print("{:^13}".format("---->"),end="")
        for col_sep in range(n//3):
                print(f"{Fore.RED}|{Fore.BLACK} "+" | ".join((str(num) if num>0 else " " for num in solution[n//2,col_sep*n//3:(col_sep+1)*n//3])),end="")
        print(f"{Fore.RED} |{Fore.BLACK}")
        for row in range(n//2+1,n):
            for col_sep in range(n//3):
                print(f"{Fore.RED}|{Fore.BLACK} "+" | ".join((str(num) if num>0 else " " for num in puzzle[row,col_sep*n//3:(col_sep+1)*n//3])),end="")
            print(f"{Fore.RED} |{Fore.BLACK}",end="")
            print("\t\t",end="")
            for col_sep in range(n//3):
                print(f"{Fore.RED}|{Fore.BLACK} "+" | ".join((str(num) if num>0 else " " for num in solution[row,col_sep*n//3:(col_sep+1)*n//3])),end="")
            print(f"{Fore.RED} |{Fore.BLACK}")
            if (row+1)%3==0:
                print("  "*(n)+"\t\t"+"  "*(n))
        
    else:
        print(f"The sudoku\n{puzzle}\nis not solvable.")

