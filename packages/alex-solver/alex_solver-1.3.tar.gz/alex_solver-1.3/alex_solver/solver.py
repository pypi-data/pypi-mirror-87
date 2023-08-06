class solver(object):

    def twoSum(nums, target):
        """
        https://leetcode.com/problems/two-sum/
        Given an array of integers nums and an integer target,
        return indices of the two numbers such that they add up to target.

        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        leftovers = {}
        for i, v in enumerate(nums):
            diff = target - v
            if diff in leftovers:
                return [leftovers[diff], i]
            if v not in leftovers:
                leftovers[v] = i
        return []


    def threeSum(self, nums):
        """
        https://leetcode.com/problems/3sum/
        Given an array nums of n integers, are there elements a, b, c in nums
        such that a + b + c = 0? Find all unique triplets in the array which
        gives the sum of zero.
        Notice that the solution set must not contain duplicate triplets.

        :type nums: List[int]
        :rtype: List[List[int]]
        """
        trip_list = set()
        duplicates = set()
        seen = {}

        for i, v1 in enumerate(nums):
            if v1 not in duplicates:
                duplicates.add(v1)
                for j, v2 in enumerate(nums[i+1:]):
                    temp = -(v1+v2)
                    if temp in seen and seen[temp] == i:
                        trip_list.add(tuple(sorted((v1,v2,temp))))
                    seen[v2] = i
        return trip_list


    def maxSubArray(self, nums):
        """
        https://leetcode.com/problems/maximum-subarray/
        Given an integer array nums, find the contiguous subarray (containing at
        least one number) which has the largest sum and return its sum.

        :type nums: List[int]
        :rtype: int
        """
        n = len(nums)
        curr_sum = max_sum = nums[0]

        for i in range(1, n):
            curr_sum = max(nums[i], curr_sum+nums[i])
            max_sum = max(max_sum, curr_sum)

        return max_sum


    def findDisappearedNumbers(nums):
        """
        https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/
        Given an array of integers where 1 ≤ a[i] ≤ n (n = size of array),
        some elements appear twice and others appear once.
        Find all the elements of [1, n] inclusive that do not appear in this array.

        :type nums: List[int]
        :rtype: List[int]
        """
        return set(range(1,len(nums)+1)) - set(nums)


    def majorityElement(nums):
        """
        https://leetcode.com/problems/majority-element/
        Given an array of size n, find the majority element.
        The majority element is the element that appears more than ⌊ n/2 ⌋ times.

        :type nums: List[int]
        :rtype: int
        """
        return max(set(nums), key=nums.count)


    def moveZeroes(nums):
        """
        https://leetcode.com/problems/move-zeroes/
        Given an array nums, write a function to move all 0's
        to the end of it while maintaining the relative order of the non-zero elements.

        :type nums: List[int]
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        for i in range(len(nums)):
            if nums[i] == 0:
                nums.append(nums.pop(nums.index(nums[i])))


    def productExceptSelf(self, nums):
        """
        https://leetcode.com/problems/product-of-array-except-self/
        Given an array nums of n integers where n > 1,  return an array output
        such that output[i] is equal to the product of all the elements of nums
        except nums[i].
        Note: Please solve it without division and in O(n).

        :type nums: List[int]
        :rtype: List[int]
        """
        l = len(nums)
        ans = [1] * l
        for i in range(1, l):
            ans[i] = ans[i-1]*nums[i-1]

        r = 1
        for i in range(l-1, -1, -1):
            ans[i] = ans[i] * r
            r *= nums[i]

        return ans


    def singleNumber(nums):
        """
        https://leetcode.com/problems/single-number/
        Given a non-empty array of integers nums,
        every element appears twice except for one. Find that single one.

        :type nums: List[int]
        :rtype: int
        """
        a = 0
        for i in nums:
            a ^= i
        return a


    def lengthOfLongestSubstring(s):
        """
        https://leetcode.com/problems/longest-substring-without-repeating-characters/
        Given a string s, find the length of the longest substring without repeating characters.

        :type s: str
        :rtype: int
        """
        dicts = {}
        maxlength = start = 0
        for i,value in enumerate(s):
            # decide where to start (think of "abba")
            if value in dicts:
                start = max(start, dicts[value] + 1)
            # current length of substring
            num = i - start + 1
            # update maxlength
            maxlength = max(maxlength, num)
            # record latest index of this letter
            dicts[value] = i
        return maxlength


    def longestPalindrome(self, s):
        """
        https://leetcode.com/problems/longest-palindromic-substring/
        Given a string s, return the longest palindromic substring in s.

        :type s: str
        :rtype: str
        """
        self.maxLength = 1
        self.start = 0

        def expand(self,low, high):
            while low >= 0 and high < len(s) and s[low] == s[high]:
                if high - low + 1 > self.maxLength:
                    self.start = low
                    self.maxLength = high - low + 1
                low -= 1
                high += 1

        # expand from every character as center point
        for i in range(1, len(s)):
            # Find the longest even length palindrome with center points i-1 and i.
            expand(self,i-1,i)
            # Find the longest odd length palindrome with center point i
            expand(self,i-1,i+1)

        return s[self.start:self.start + self.maxLength]


    def maxProfit(prices):
        """
        https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
        Say you have an array for which the ith element is the price of a given stock on day i.
        If you were only permitted to complete at most one transaction (i.e.,
        buy one and sell one share of the stock), design an algorithm to find the maximum profit.
        Note that you cannot sell a stock before you buy one.

        :type prices: List[int]
        :rtype: int
        """
        if not prices:
            return 0

        min_price = prices[0]
        max_profit = 0

        for i, v in enumerate(prices):
            if v < min_price:
                min_price = v
            elif v - min_price > max_profit:
                max_profit = v - min_price

        return max_profit


    def climbStairs(n):
        """
        https://leetcode.com/problems/climbing-stairs/
        You are climbing a staircase. It takes n steps to reach the top.
        Each time you can either climb 1 or 2 steps.
        In how many distinct ways can you climb to the top?

        :type n: int
        :rtype: int
        """
        if (n == 1): return 1

        first = 1
        second = 2
        for i in range(3,n+1):
            third = first + second
            first = second
            second = third

        return second


    def rob(nums):
        """
        https://leetcode.com/problems/house-robber/
        You are a professional robber planning to rob houses along a street.
        Each house has a certain amount of money stashed, the only constraint
        stopping you from robbing each of them is that adjacent houses have
        security system connected and it will automatically contact the police
        if two adjacent houses were broken into on the same night.

        Given a list of non-negative integers representing the amount of money
        of each house, determine the maximum amount of money you can rob tonight
        without alerting the police.

        :type nums: List[int]
        :rtype: int
        """
        prev_max = 0
        curr_max = 0
        for i in range(len(nums)):
            temp = curr_max
            curr_max = max(prev_max + nums[i], curr_max)
            prev_max = temp

        return curr_max


    def trap(height):
        """
        https://leetcode.com/problems/trapping-rain-water/
        Given n non-negative integers representing an elevation map where the
        width of each bar is 1, compute how much water it can trap after raining.

        :type height: List[int]
        :rtype: int
        """
        if not height:
            return 0

        ans = 0
        size = len(height)
        left_max = [0] * size
        right_max = [0] * size
        left_max[0] = height[0]
        right_max[-1] = height[-1]
        for i in range(1, size):
            left_max[i] = max(height[i], left_max[i-1])

        for i in range(size-2, -1, -1):
            right_max[i] = max(height[i], right_max[i+1])

        for i in range(size):
            ans += min(left_max[i], right_max[i]) - height[i]
        return ans


    def numIslands(grid):
        """
        https://leetcode.com/problems/number-of-islands/
        Given an m x n 2d grid map of '1's (land) and '0's (water),
        return the number of islands.
        An island is surrounded by water and is formed by connecting adjacent
        lands horizontally or vertically. You may assume all four edges of
        the grid are all surrounded by water.

        :type grid: List[List[str]]
        :rtype: int
        """
        nr = len(grid)
        nc = len(grid[0])
        num_islands = 0

        def dfs(grid, r, c):
            if (r < 0 or c < 0 or r >= nr or c >= nc or grid[r][c] == '0'):
                return

            grid[r][c] = '0'
            dfs(grid, r-1, c)
            dfs(grid, r+1, c)
            dfs(grid, r, c-1)
            dfs(grid, r, c+1)

        if (not grid or len(grid) == 0): return 0

        for r in range(nr):
            for c in range(nc):
                if (grid[r][c] == '1'):
                    num_islands += 1
                    dfs(grid, r, c)

        return num_islands


# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
    def addTwoNumbers(self, l1, l2, c = 0):
        """
        https://leetcode.com/problems/add-two-numbers/
        Given two non-empty linked lists representing two non-negative integers.
        The digits are stored in reverse order, and each of their nodes contains a single digit.
        Add the two numbers and return the sum as a linked list.

        Assume the two numbers do not contain any leading zero, except the number 0 itself.
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        val = l1.val + l2.val + c
        c = val // 10
        ret = ListNode(val%10)

        if (l1.next != None or l2.next != None or c != 0):
            if l1.next == None:
                l1.next = ListNode(0)
            if l2.next == None:
                l2.next = ListNode(0)
            ret.next = self.addTwoNumbers(l1.next, l2.next, c)
        return ret


    def reverseList(self, head):
        """
        https://leetcode.com/problems/reverse-linked-list/
        Reverse a singly linked list.

        :type head: ListNode
        :rtype: ListNode
        """
        if not head or not head.next:
            return head
        p = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return p


    def mergeTwoLists(self, l1, l2):
        """
        https://leetcode.com/problems/merge-two-sorted-lists/
        Merge two sorted linked lists and return it as a new sorted list.
        The new list should be made by splicing together the nodes of the first two lists.

        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        if l1 is None:
            return l2
        elif l2 is None:
            return l1
        elif l1.val < l2.val:
            l1.next = self.mergeTwoLists(l1.next, l2)
            return l1
        else:
            l2.next = self.mergeTwoLists(l1, l2.next)
            return l2


# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
    def mergeTrees(self, t1, t2):
        """
        https://leetcode.com/problems/merge-two-binary-trees/
        Given two binary trees and imagine that when you put one of them to cover the other,
        some nodes of the two trees are overlapped while the others are not.
        You need to merge them into a new binary tree. The merge rule is that if two nodes overlap,
        then sum node values up as the new value of the merged node.
        Otherwise, the NOT null node will be used as the node of new tree.

        :type t1: TreeNode
        :type t2: TreeNode
        :rtype: TreeNode
        """
        if not t1:
            return t2
        if not t2:
            return t1
        t = TreeNode(t1.val+t2.val)
        t.left = self.mergeTrees(t1.left, t2.left)
        t.right = self.mergeTrees(t1.right, t2.right)
        return t


    def maxDepth(self, root):
        """
        https://leetcode.com/problems/maximum-depth-of-binary-tree/
        Given a binary tree, find its maximum depth.
        The maximum depth is the number of nodes along the longest path
        from the root node down to the farthest leaf node.

        :type root: TreeNode
        :rtype: int
        """
        if root is None:
            return 0
        else:
            left_h = self.maxDepth(root.left)
            right_h = self.maxDepth(root.right)
            return max(left_h, right_h) + 1


    def diameterOfBinaryTree(self, root):
        """
        https://leetcode.com/problems/diameter-of-binary-tree/
        Given a binary tree, you need to compute the length of the diameter of the tree.
        The diameter of a binary tree is the length of the longest path between
        any two nodes in a tree. This path may or may not pass through the root.

        :type root: TreeNode
        :rtype: int
        """

        self.path_bt_nodes = 0
        def depth(root):
            if not root: return 0
            left = depth(root.left)
            right = depth(root.right)
            # path
            self.path_bt_nodes = max(self.path_bt_nodes, left + right)
            # depth
            return max(left, right) + 1

        depth(root)
        return self.path_bt_nodes


    def invertTree(self, root):
        """
        https://leetcode.com/problems/invert-binary-tree/
        Invert a binary tree.

        :type root: TreeNode
        :rtype: TreeNode
        """
        if root:
            root.left, root.right = self.invertTree(root.right), self.invertTree(root.left)
        return root


    def isSymmetric(self, root):
        """
        https://leetcode.com/problems/symmetric-tree/
        Given a binary tree, check whether it is a mirror
        of itself (ie, symmetric around its center).

        :type root: TreeNode
        :rtype: bool
        """
        return self.isMirror(root, root)


    def isMirror(self, t1, t2):
        """
        helper function for isSymmetric
        """
        if not t1 and not t2: return True
        if not t1 or not t2: return False
        return t1.val == t2.val and self.isMirror(t1.right, t2.left) and self.isMirror(t1.left, t2.right)


class MinStack(object):
    """
    https://leetcode.com/problems/min-stack/
    Design a stack that supports push, pop, top, and retrieving the minimum
    element in constant time.

    push(x) -- Push element x onto stack.
    pop() -- Removes the element on top of the stack.
    top() -- Get the top element.
    getMin() -- Retrieve the minimum element in the stack.
    """
    def __init__(self):
        """
        initialize your data structure here.
        """
        self.arr = []

    def push(self, x):
        """
        :type x: int
        :rtype: None
        """
        self.arr.append(x)

    def pop(self):
        """
        :rtype: None
        """
        return self.arr.pop()

    def top(self):
        """
        :rtype: int
        """
        return self.arr[-1]

    def getMin(self):
        """
        :rtype: int
        """
        return min(self.arr)


class LRUCache(object):
    """
    https://leetcode.com/problems/lru-cache/solution/
    Design a data structure that follows the constraints of a
    Least Recently Used (LRU) cache.
    """

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.size = capacity
        self.cache_dict = {}
        self.LRU_dict = {}

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key in self.cache_dict:
            for key1, value1 in self.LRU_dict.items():
                self.LRU_dict[key1] = value1 + 1
            self.LRU_dict[key] = 1
            return self.cache_dict[key]
        else:
            return -1

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """

        for key1, value1 in self.LRU_dict.items():
            self.LRU_dict[key1] = value1 + 1
        self.cache_dict[key] = value
        self.LRU_dict[key] = 1

        if len(self.cache_dict) == self.size + 1:
            max_key = max(self.LRU_dict, key=self.LRU_dict.get)
            del self.cache_dict[max_key]
            del self.LRU_dict[max_key]
