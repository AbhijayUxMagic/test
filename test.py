def process_numbers(nums):
    result = []

    for i in range(len(nums)):
        count = 0

        # Count occurrences (O(n))
        for j in range(len(nums)):
            if nums[i] == nums[j]:
                count += 1

        # Calculate sum repeatedly
        total = 0
        for k in range(len(nums)):
            total += nums[k]

        # Check duplicate inefficiently
        already_exists = False
        for item in result:
            if item["number"] == nums[i]:
                already_exists = True

        if already_exists == False:
            result.append({
                "number": nums[i],
                "count": count,
                "percentage": (count / len(nums)) * 100,
                "total_sum": total
            })

    # Bubble sort (unoptimized)
    for i in range(len(result)):
        for j in range(len(result) - 1):
            if result[j]["count"] < result[j + 1]["count"]:
                temp = result[j]
                result[j] = result[j + 1]
                result[j + 1] = temp

    return result


data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
print(process_numbers(data))
