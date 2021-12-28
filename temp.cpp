#include<iostream>
using namespace std;


 struct ListNode {
     int val;
     ListNode *next;
     ListNode() : val(0), next(nullptr) {}
     ListNode(int x) : val(x), next(nullptr) {}
     ListNode(int x, ListNode *next) : val(x), next(next) {}
 };
 
 int main(){
     ListNode node(50);
     ListNode *head, *curr;
     curr =  head = &node;
     for(int i = 0; i < 5; i++){
         ListNode node(i);
         curr->next = &node;
         curr = curr->next;
     }
     curr->next = NULL;
     while(head){
         cout<<head->val<<" ";
         head = head->next;
     }
     cout<<"\n";
 }