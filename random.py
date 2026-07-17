def product_of_array(nums: list[int]) -> list[int]:
    """
    Input: nums = [1, 2, 3, 4]

    1, 2, 6, 24
    24 ,24, 12 , 4

    Output: [24, 12, 8, 6]
    """
    n = len(nums)
    if n <= 1:
        return nums
    
    output = nums.copy()
    for i in range(1, n):
        output[i] = output[i-1] * nums[i]

    output[-1] = output[-2]

    right_prod = nums[-1]

    for i in range(n-2, 0, -1):
        output[i] = output[i-1] * right_prod
        right_prod *= nums[i]

    output[0] = right_prod

    return output