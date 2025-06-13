#modelo em - O(n^2)

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Testa todos os pares possíveis
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        
        # Como o problema garante que existe uma solução,
        # nunca chegará aqui
        return []

# Exemplo de uso:
# nums = [2,7,11,15], target = 9
# i=0, j=1: nums[0] + nums[1] = 2 + 7 = 9 ✓
# Retorna [0,1]


#modelo em - O(n)
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Dicionário para armazenar: valor -> índice
        seen = {}
        
        for i, num in enumerate(nums):
            # Calcula o complemento necessário
            complement = target - num
            
            # Se o complemento já foi visto antes, encontramos a resposta
            if complement in seen:
                return [seen[complement], i]
            
            # Armazena o número atual e seu índice
            seen[num] = i
        
        # Como o problema garante que existe uma solução,
        # nunca chegará aqui
        return []

# Exemplo passo a passo com nums = [2,7,11,15], target = 9:
# i=0, num=2, complement=9-2=7
# 7 não está em seen
# seen = {2: 0}
#
# i=1, num=7, complement=9-7=2
# 2 está em seen! seen[2] = 0
# Retorna [0, 1]