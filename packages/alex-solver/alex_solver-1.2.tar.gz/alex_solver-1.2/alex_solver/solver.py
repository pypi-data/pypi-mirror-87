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
            if value in dicts:
                sums = dicts[value] + 1
                if sums > start:
                    start = sums
            num = i - start + 1
            if num > maxlength:
                maxlength = num
            dicts[value] = i
        return maxlength


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
