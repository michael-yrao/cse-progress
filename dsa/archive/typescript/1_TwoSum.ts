function twoSum(nums: number[], target: number): number[] 
{
    /** Insert num into map, check if diff exist in map */
    let map = new Map<number,number>();
    for(let i=0;i<nums.length;i++)
    {
        let diff = target - nums[i];
        // We can use ! as a way to assert that the value will not be undefined
        if(map.has(diff) && map.get(diff) != i) return [i, map.get(diff)!];

        map.set(nums[i],i);
    }
    return [-1,-1];
}