#PythonでOne-Max問題を解く
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

#ハイパーパラメータ
generation = 300 # 何世代実行するか
gene_length = 50 #遺伝子長
pool_size = 100 #個体数
mutation_rate = 0.01 #突然変異率

#遺伝子の作成
#遺伝子は0と1からランダムで選ばれる
def init_gene():
    gene = [[random.randint(0, 1) for i in range(gene_length)] for j in range(pool_size)]
    return gene

#適応度の計算
#1の個数を適応度と定義する
def fitness_cal(gene):
    fitness = []

    for i in range(pool_size):
        one_num = 0
        for j in range(gene_length):
            if gene[i][j] == 1:
                one_num += 1
        fitness.append(one_num)
    return fitness

#交叉
def cross_over(gene):
    copy_gene = copy.deepcopy(gene)

    for i in range(pool_size):
        partner = random.randint(0, pool_size - 1) #交叉させる個体の相方を決める
        cross_point = random.randint(0, gene_length - 2) #交叉する点を決める
        for j in range(cross_point, gene_length):
            copy_gene[i][j] = gene[partner][j]
            copy_gene[partner][j] = gene[i][j]
    
    gene = copy.deepcopy(copy_gene)

#突然変異
def mutation(gene):
    for i in range(pool_size):
        for j in range(gene_length):
            #乱数がmutation_rate以下なら突然変異
            randnum = random.random()
            if randnum <= mutation_rate:
                gene[i][j] = 1 - gene[i][j] #ビット反転

#選択
def select(gene, fitness):
    copy_gene = copy.deepcopy(gene)
    copy_fitness = copy.copy(fitness)
    sum_fitness = sum(fitness)
    
    #優秀な遺伝子を残す
    elite = fitness.index(max(fitness))
    failure = fitness.index(min(fitness))
    for i in range(pool_size):
        for j in range(gene_length):
            gene[failure][j] = gene[elite][j]
    fitness[failure] = fitness[elite]
    

    
    #ルーレット選択
    for i in range(pool_size):
        randnum = random.randint(0, sum_fitness)
        for selected_gene in range(pool_size):
            randnum -= fitness[selected_gene]
            if randnum <= 0:
                break
    
        for j in range(gene_length):
            copy_gene[i][j] = gene[selected_gene][j]
            
        copy_fitness[i] = fitness[selected_gene]

    gene = copy.deepcopy(copy_gene)
    fitness = copy.copy(copy_fitness)
    



def result_plt(result_max_fitness, result_min_fitness, result_ava_fitness):
    x = [i for i in range(1, generation + 1)]
    Max = result_max_fitness
    Min = result_min_fitness
    Ava = result_ava_fitness

    plt.suptitle("世代数に対する適応度の推移", fontname = "MS Gothic")
    plt.xlabel("世代", fontname = "MS Gothic")
    plt.ylabel("適応度", fontname = "MS Gothic")
    plt.plot(x, Max, color = "red", label ="最大値")
    plt.plot(x, Ava, color = "green", label ="平均値")
    plt.plot(x, Min, color = "blue", label ="最小値")
    plt.legend(loc = 0, prop={"family":"MS Gothic"})
    plt.show()

def main():
    result_max_fitness = []
    result_min_fitness = []
    result_ava_fitness = []
    gene = init_gene()
    fitness = fitness_cal(gene)
    result_max_fitness.append(max(fitness))
    result_min_fitness.append(min(fitness))
    result_ava_fitness.append(sum(fitness) / pool_size)
    generation_count = 2
    print("generatation" + str(1))
    print("適応度の最大値は" + str(max(fitness)) + " 適応度の最小値は" + str(min(fitness)) + "適応度の平均値は" + str(sum(fitness) / pool_size))
    while (generation_count <= generation):

        print("generatation" + str(generation_count))

        cross_over(gene)
        mutation(gene)
        select(gene, fitness)
        fitness = fitness_cal(gene)
        result_max_fitness.append(max(fitness))
        result_min_fitness.append(min(fitness))
        result_ava_fitness.append(sum(fitness) / pool_size)


        print("適応度の最大値は" + str(max(fitness)) + " 適応度の最小値は" + str(min(fitness)) + "適応度の平均値は" + str(sum(fitness) / pool_size))

        generation_count += 1

    result_plt(result_max_fitness, result_min_fitness, result_ava_fitness)

if __name__ == "__main__":
    main()


