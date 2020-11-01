from tkinter import Tk
from tkinter.ttk import Frame, Button, Label
import tkinter as tk
from PIL import Image, ImageTk
import os.path
from os import path
import json
import random
import time

class BlackJack(Frame):
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.bank_account = 1000
        self.load_screen_contents = []
        self.deck = []
        self.pot = 0
        self.play_screen_contents = []
        self.can_hold = False
        self.bet_amt = 1
        self.dealer_cards = []
        self.user_cards = []
        self.dealer_card_totala = 0
        self.dealer_card_totalA = 0
        self.dealer_card_total_showa = 0
        self.dealer_card_total_showA = 0
        self.dealer_card_total_showing = ''
        self.user_card_totala = 0
        self.user_card_totalA = 0
        self.user_card_total_showing = ''
        self.last_game_won = False
        self.last_game_push = False
        self.last_game_pot = 0
        self.betting_buttons = []
        self.dealer_cards_images=[]
        self.user_cards_images = []
        self.user_number_of_cards = 0
        self.dealer_number_of_cards = 0
        self.dealer_wins = False
        self.user_wins = False
        self.game_is_push = False
        self.user_busted = False
        self.dealer_busted = False
        self.hhbut = []
        self.user_blkjack = False
        self.dealer_blkjack = False
        self.user_final_count=None
        self.dealer_final_count=None
        self.winnings=0
        self.end_match_screen_buttons=[]
        self.number_of_decks=5
        self.last_game_winnings=0
        self.insurance_button = None
        self.insurance_offered=False
        self.has_insurance=False
        #variables above this line
        self.initUI()

    def new_game_or_restore(self):
        #Add Spade cards image for load screen 
        new_game_image = Image.open('./images/honors_spade-14.png')
        ngi_width, ngi_height = new_game_image.size
        new_game_image = ImageTk.PhotoImage(new_game_image.resize((ngi_width//6, ngi_height//6), Image.LANCZOS))
        new_game_image_label = Label(image=new_game_image)
        new_game_image_label.image = new_game_image
        new_game_image_label.place(x=200, y=150)
        #Add new game button for load screen (red button)
# here i am
        image = Image.open("./images/newgame.png")
        i_width, i_height = image.size
        image = ImageTk.PhotoImage(image.resize((int(i_width//20), int(i_height//20)), Image.LANCZOS))
        new_game_but = tk.Button(command=lambda: [self.init_game()])
        new_game_but.config(image=image, bg="darkgreen", bd=0)
        new_game_but.image = image
        new_game_but.place(x=200, y=400)
        #Add restore game button for load screen (green button)
        image = Image.open("./images/continue.png")
        i_width, i_height = image.size
        image = ImageTk.PhotoImage(image.resize((int(i_width//3.25), int(i_height//3.25)), Image.LANCZOS))
        restore_game_but = tk.Button(command=lambda: [restore(self), self.init_game()])
        restore_game_but.config(image=image, bg="darkgreen", bd=0)
        restore_game_but.image = image
        restore_game_but.place(x=435, y=400)
        #add all widgets to a list
        self.load_screen_contents.append(new_game_image_label)
        self.load_screen_contents.append(new_game_but)
        self.load_screen_contents.append(restore_game_but)
        
    def kill_ngr(self):
        #Clear the Load Screen
        for button in self.load_screen_contents:
            button.destroy()

    def make_deck(self):
        if(not self.deck):
            #make all the card values
            card_values=[]
            for i in range(2,15):
                if(i==11):
                    card_string="J"
                elif(i == 12):
                    card_string = "Q"
                elif(i == 13):
                    card_string = "K"
                elif(i == 14):
                    card_string = "A"
                else:
                    card_string=str(i)
                card_values.append(card_string)
            #makes Clubs
            for card in card_values:
                self.deck.append(card+"C")
            #makes Diamonds
            for card in card_values:
                self.deck.append(card+"D")
            #makes Hearts
            for card in card_values:
                self.deck.append(card+"H")
            #makes Spades
            for card in card_values:
                self.deck.append(card+"S")
            #make number_of_decks amount of decks
            self.deck=[card for card in self.deck for _ in range(self.number_of_decks)]   
            #shuffle deck
            random.shuffle(self.deck)

    def dealer_play(self):

        self.kill_hit_hold_buttons()
        #define when dealer takes a hit
        while((self.dealer_card_totalA < 17 and self.dealer_card_totalA < 21) or (self.dealer_card_totala < 17 and self.dealer_card_totala < 21)):
            if(self.dealer_card_totalA == self.dealer_card_totala):  # if no ace and less than 17 hit
                if self.dealer_card_total_showA < 17:
                    self.dealer_hit()
                    
            # if Big Ace (11) is under 21 and under 17 hit
            elif(self.dealer_card_totalA < 17 and self.dealer_card_totalA < 21):
                self.dealer_hit()
            #if 21 with Big Ace Hold
            elif self.dealer_card_totalA==21:
                break
            # if little Ace (1) is under 21 and under 17 hit
            elif(self.dealer_card_totala < 17 and self.dealer_card_totala < 21):
                self.dealer_hit()

        self.check_scores()
        self.hand_results()


    def update_card_points_user(self):
        self.user_card_totala=0
        self.user_card_totalA=0
        #adds up points for all the card take small(1) value for a
        for card in self.user_cards:
            if card[:-1] == "J" or card[:-1] == "Q" or card[:-1] == "K":
                self.user_card_totala+=10
            elif card[:-1] == "A":
                self.user_card_totala+=1
            else:
                self.user_card_totala += int(card[:-1])
        #adds up points for all the card take large (11) value for A
        just_one_ace = True
        for card in self.user_cards:
            if card[:-1] == "J" or card[:-1] == "Q" or card[:-1] == "K":
                self.user_card_totalA += 10
            elif card[:-1] == "A":
                if(just_one_ace):
                    self.user_card_totalA += 11
                    just_one_ace = False
                else:
                    self.user_card_totalA += 1
            else:
                self.user_card_totalA += int(card[:-1])
        self.make_user_card_showing_string()

    def make_user_card_showing_string(self):
        #returns string of possible values of user cards
        show_string=str(self.user_card_totala)
        if(self.user_card_totalA < 21 and self.user_card_totalA != self.user_card_totala):
            show_string += " or " + str(self.user_card_totalA)
        self.user_card_total_showing = show_string


    def update_card_points_dealer(self):
        self.dealer_card_totala = 0
        self.dealer_card_totalA=0
        #adds up points for all the card take small(1) value for a
        just_one_ace=True
        for card in self.dealer_cards:
            if card[:-1] == "J" or card[:-1] == "Q" or card[:-1] == "K":
                self.dealer_card_totala+=10
            elif card[:-1] == "A":
                self.dealer_card_totala += 1
            else:
                self.dealer_card_totala += int(card[:-1])
        #adds up points for all the card take large (11) value for A
        for card in self.dealer_cards:
            if card[:-1] == "J" or card[:-1] == "Q" or card[:-1] == "K":
                self.dealer_card_totalA += 10
            elif card[:-1] == "A":
                if(just_one_ace):
                    self.dealer_card_totalA += 11
                    just_one_ace = False
                else:
                    self.dealer_card_totalA += 1
            else:
                self.dealer_card_totalA += int(card[:-1])
        self.update_card_points_dealer_showing()
        self.make_dealer_card_showing_string()

    def update_card_points_dealer_showing(self):
        #get point for display purposes of what the deal shows
        self.dealer_card_total_showa = 0
        self.dealer_card_total_showA = 0
        #adds up points for all the card take small(1) value for a
        for card in self.dealer_cards[1:]:
            if card[:-1] == "J" or card[:-1] == "Q" or card[:-1] == "K":
                self.dealer_card_total_showa += 10
            elif card[:-1] == "A":
                self.dealer_card_total_showa += 1
            else:
                self.dealer_card_total_showa += int(card[:-1])
        #adds up points for all the card take large (11) value for A
        for card in self.dealer_cards[1:]:
            if card[:-1] == "J" or card[:-1] == "Q" or card[:-1] == "K":
                self.dealer_card_total_showA += 10
            elif card[:-1] == "A":
                self.dealer_card_total_showA += 11
            else:
                self.dealer_card_total_showA += int(card[:-1])

        
        self.make_dealer_card_showing_string()

    def make_dealer_card_showing_string(self):
        #returns string of possible values of dealers cards that are showing
        show_string=str(self.dealer_card_total_showa)
        if(self.dealer_card_total_showA < 21 and self.dealer_card_total_showA != self.dealer_card_total_showa):
            show_string += " or " + str(self.dealer_card_total_showA)
        self.dealer_card_total_showing = show_string

    def check_scores(self):
        #check for highest non busted score for user and dealer
        if(self.user_card_totalA <= 21):
            self.user_final_count = self.user_card_totalA
        else:
            self.user_final_count = self.user_card_totala

        if(self.dealer_card_totalA <= 21):
            self.dealer_final_count = self.dealer_card_totalA
        else:
            self.dealer_final_count = self.dealer_card_totala
        #compare scores
        if self.user_final_count == self.dealer_final_count:
            self.game_is_push = True
        elif self.user_final_count <= 21 and (self.user_final_count > self.dealer_final_count or self.dealer_busted):
            self.user_wins=True
        elif self.dealer_final_count <= 21 and (self.user_final_count < self.dealer_final_count or self.user_busted):
            self.dealer_wins=True

        #if both players bust is a push
        if(self.user_busted & self.dealer_busted):
            self.game_is_push = True
            

    def make_insurance_offer(self):
        self.insurance_offered=True
        self.make_hit_hold_buttons()


    def check_for_blackjack(self):
        #checks users for a blackjack
        if(self.user_cards[0][:-1] in ["J", "K", "Q", "10"] and self.user_cards[1][:-1] == "A") or (self.user_cards[1][:-1] in ["J", "K", "Q", "10"] and self.user_cards[0][:-1] == "A"):
            #blackjack for the user
            self.user_blkjack=True
        #checks Dealer for blackjack
        if(self.dealer_cards[0][:-1] in ["J", "K", "Q", "10"] and self.dealer_cards[1][:-1] == "A") or (self.dealer_cards[1][:-1] in ["J", "K", "Q", "10"] and self.dealer_cards[0][:-1] == "A"):
            #blackjack for the dealer
            self.dealer_blkjack = True

        if self.dealer_blkjack and self.user_blkjack:
            self.game_is_push = True
            self.hand_results()
        elif self.user_blkjack:
            self.user_wins=True
            self.hand_results()
        elif self.dealer_blkjack:
            self.dealer_wins = True
            self.hand_results()
   
    def hand_results(self):
        self.last_game_pot=self.pot
        self.last_game_won=self.user_wins
        self.last_game_push = self.game_is_push
        #find the amount of winnings and add it to the bank account
        if(self.user_blkjack and not self.game_is_push):
            self.winnings=self.pot*1.5 #pays 3:2
        elif(self.dealer_blkjack and self.has_insurance):
            self.winnings=self.pot
        elif (self.user_wins):
            self.winnings=self.pot
        elif(self.game_is_push):
            self.winnings=self.pot/2
        elif(self.dealer_wins):
            self.winnings=0
        self.bank_account+=self.winnings
        self.kill_game_screen()
        self.show_end_match_choices()
        self.last_game_winnings=self.winnings
    
    def kill_game_screen(self):
        for button in self.play_screen_contents:
            button.destroy()
    def dealer_flip_hold_card(self):
        self.dealer_number_of_cards=1
        for card in self.dealer_cards:
            self.make_dealer_card_show(card)
            self.dealer_number_of_cards+=1

    def show_end_match_choices(self):
        self.dealer_flip_hold_card()
        #Add Spade cards image for end screen
        new_game_image = Image.open('./images/honors_spade-14.png')
        ngi_width, ngi_height = new_game_image.size
        new_game_image = ImageTk.PhotoImage(new_game_image.resize(
            (ngi_width//6, ngi_height//6), Image.LANCZOS))
        new_game_image_label = Label(image=new_game_image)
        new_game_image_label.image = new_game_image
        new_game_image_label.place(x=200, y=175)
        
        #Add button for New Game
        image = Image.open("./images/newgame.png")
        i_width, i_height = image.size
        image = ImageTk.PhotoImage(image.resize((int(i_width//20), int(i_height//20)), Image.LANCZOS))
        new_game_but = tk.Button(command=lambda: [self.start_new_game()])
        new_game_but.config(image=image, bg="darkgreen", bd=0)
        new_game_but.image = image
        new_game_but.place(x=600, y=100)

        #Add button for Next Hand
        if(self.bank_account>=1):
            image = Image.open("./images/nexthand.png")
            i_width, i_height = image.size
            image = ImageTk.PhotoImage(image.resize((int(i_width//3.25), int(i_height//3.25)), Image.LANCZOS))
            next_hand_but = tk.Button(command=lambda: [self.continue_game()])
            next_hand_but.config(image=image, bg="darkgreen", bd=0)
            next_hand_but.image = image
            next_hand_but.place(x=600, y=100)
            next_hand_but.place(x=600, y=250)

        #Add Save and Quit
        image = Image.open("./images/save.png")
        i_width, i_height = image.size
        image = ImageTk.PhotoImage(image.resize((int(i_width//20), int(i_height//20)), Image.LANCZOS))
        quit_but = tk.Button(command=lambda: [save(self), self.master.destroy()])
        quit_but.config(image=image, bg="darkgreen", bd=0)
        quit_but.image = image
        quit_but.place(x=600, y=400)
        
        #show the Final score to user        
        win_lose_string=''
        if(self.user_wins):
            win_lose_string = 'You Have Won $'+str(self.winnings)
        elif(self.game_is_push or (self.dealer_blkjack and self.has_insurance)):
            win_lose_string = 'It was a Draw'
        else:
            win_lose_string = 'You Have Lost'
        results_txt = tk.Text(height=3, width=20, fg="grey", bg="black", font='Helvetica 12 bold',bd=0)
        results_txt.insert(tk.END, f"{win_lose_string}\n Your count: {self.user_final_count}\nDealer count: {self.dealer_final_count}")
        results_txt.tag_configure("center", justify='center')
        results_txt.tag_add("center", "1.0", "end")
        results_txt.place(x=10, y=175)

        if(self.user_blkjack):
            results_txt2 = tk.Text(height=2, width=20, fg="grey", bg="black", font='Helvetica 12 bold',bd=0)
            results_txt2.insert(tk.END, f"You won by\nBLACKJACK")
            results_txt2.tag_configure("center", justify='center')
            results_txt2.tag_add("center", "1.0", "end")
            results_txt2.place(x=10, y=250)
            self.end_match_screen_buttons.append(results_txt2)
        
        #show the New Bank Balance to user
        balance_txt = tk.Text(height=1, width=20, fg="grey",
                              bg="black", font='Helvetica 12 bold', bd=0)
        balance_txt.insert(tk.END, f"You Have: ${int(self.bank_account)}")
        balance_txt.tag_configure("center", justify='center')
        balance_txt.tag_add("center", "1.0", "end")
        balance_txt.place(x=10, y=375)
        
        #add all widgets to a list
        self.end_match_screen_buttons.append(balance_txt)
        self.end_match_screen_buttons.append(results_txt)
        
        self.end_match_screen_buttons.append(new_game_but)
        self.end_match_screen_buttons.append(next_hand_but)
        self.end_match_screen_buttons.append(quit_but)
        self.end_match_screen_buttons.append(new_game_image_label)
        
    def kill_end_match_choices(self):
        #clears end match screen
        for button in self.end_match_screen_buttons:
            button.destroy()
    
    def kill_card_images(self):
        #removes all the card images
        for card in self.user_cards_images:
            card.destroy()
        for card in self.dealer_cards_images:
            card.destroy()

    def start_new_game(self):
        #start a new game from scratch
        refresh(self.root)

    def continue_game(self):
        #play next match
        self.kill_end_match_choices()
        self.kill_card_images()
        self.reset_vars()
        self.build_initial_screen()

    def reset_vars(self):
        #reset varibles needed to play another match
        self.load_screen_contents = []
        self.pot = 0
        self.play_screen_contents = []
        self.can_hold = False
        self.bet_amt = 1
        self.dealer_cards = []
        self.user_cards = []
        self.dealer_card_totala = 0
        self.dealer_card_totalA = 0
        self.dealer_card_total_showa = 0
        self.dealer_card_total_showA = 0
        self.dealer_card_total_showing = ''
        self.user_card_totala = 0
        self.user_card_totalA = 0
        self.user_card_total_showing = ''
        self.betting_buttons = []
        self.dealer_cards_images = []
        self.user_cards_images = []
        self.user_number_of_cards = 0
        self.dealer_number_of_cards = 0
        self.dealer_wins = False
        self.user_wins = False
        self.game_is_push = False
        self.user_busted = False
        self.dealer_busted = False
        self.hhbut = []
        self.user_blkjack = False
        self.dealer_blkjack = False
        self.user_final_count = None
        self.dealer_final_count = None
        self.winnings = 0
        self.end_match_screen_buttons = []
        self.insurance_button = None
        self.insurance_offered=False
        self.has_insurance=False

    def user_hit(self):
        #when user decides to hit
        uc=self.pick_card()
        self.user_cards.append(uc)
        self.user_number_of_cards += 1
        self.make_user_card_show(uc)
        self.update_card_points_user()
        self.build_play_screen()
        if(self.user_card_totala)>21:
            self.user_busted=True
            self.dealer_play()

    def dealer_hit(self):
        #when dealer decides to hit
        dc=self.pick_card()
        self.dealer_cards.append(dc)
        self.dealer_number_of_cards += 1
        self.make_dealer_card_show(dc)
        self.update_card_points_dealer()
        self.build_play_screen()
        if(self.dealer_card_totala) > 21:
            self.dealer_busted=True

    def deal_hand(self):
        #picks card and cars to list add to number of cards put card on screen, update teh display points then updates the GUI and checks for Blackjack
        uc1=self.pick_card()
        dc1=self.pick_card()
        uc2=self.pick_card()
        dc2=self.pick_card()
        self.dealer_cards.append(dc1)
        self.dealer_cards.append(dc2)
        self.user_cards.append(uc1)
        self.user_cards.append(uc2)

        self.dealer_number_of_cards += 1
        self.make_dealer_card_show(dc1, False)
        self.dealer_number_of_cards += 1
        self.make_dealer_card_show(dc2)
        self.update_card_points_dealer()

        self.user_number_of_cards += 1
        self.make_user_card_show(uc1)
        self.user_number_of_cards += 1
        self.make_user_card_show(uc2)
        self.update_card_points_user()

        self.build_play_screen()

        if dc2[0]=="A":
            self.make_insurance_offer()
    
            
        else:
            self.check_for_blackjack()
            
        
    def make_user_card_show(self, card):
        card_image = Image.open(f'./images/{card}.png')
        ci_width, ci_height = card_image.size
        card_image = ImageTk.PhotoImage(card_image.resize((ci_width//10, ci_height//10), Image.LANCZOS))
        card_image_label = Label(image=card_image)
        card_image_label.image = card_image
        #card position by card number
        if(self.user_number_of_cards==1):
            card_image_label.place(x=200, y=475)
        if(self.user_number_of_cards==2):
            card_image_label.place(x=275, y=475)
        if(self.user_number_of_cards==3):
            card_image_label.place(x=350, y=475)
        if(self.user_number_of_cards==4):
            card_image_label.place(x=425, y=475)
        if(self.user_number_of_cards==5):
            card_image_label.place(x=500, y=475)
        if(self.user_number_of_cards==6):
            card_image_label.place(x=575, y=475)
        if(self.user_number_of_cards==7):
            card_image_label.place(x=650, y=475)
        self.user_cards_images.append(card_image_label)
        #self.play_screen_contents.append(card_image_label)

    def make_dealer_card_show(self, card, showing=True):
        if(showing):
            card_image = Image.open(f'./images/{card}.png')
        else:
            card_image = Image.open(f'./images/purple_back.png')
        ci_width, ci_height = card_image.size
        card_image = ImageTk.PhotoImage(card_image.resize((ci_width//10, ci_height//10), Image.LANCZOS))
        card_image_label = Label(image=card_image)
        card_image_label.image = card_image
        #card position by card number
        if(self.dealer_number_of_cards==1):
            card_image_label.place(x=200, y=50)
        if(self.dealer_number_of_cards==2):
            card_image_label.place(x=275, y=50)
        if(self.dealer_number_of_cards==3):
            card_image_label.place(x=350, y=50)
        if(self.dealer_number_of_cards==4):
            card_image_label.place(x=425, y=50)
        if(self.dealer_number_of_cards == 5):
            card_image_label.place(x=500, y=50)
        if(self.dealer_number_of_cards == 6):
            card_image_label.place(x=575, y=50)
        if(self.dealer_number_of_cards == 7):
            card_image_label.place(x=650, y=50)
        self.dealer_cards_images.append(card_image_label)
        #self.play_screen_contents.append(card_image_label)

    def pick_card(self):
        #pulls card from the deck and if the cards run out make a new deck
        if(len(self.deck)<=1):
            self.make_deck()
        return(self.deck.pop())

    def start_dealing(self):
        self.kill_betting_button()
        self.make_hit_hold_buttons()
        self.deal_hand()

    def user_display_score(self):
        #show the card total for the user
        us_show = tk.Text(height=1, width=20, fg="grey", bd=0,bg="darkgreen", font='Helvetica 12 bold')
        us_show.insert(tk.END, f"You Have: {self.user_card_total_showing}")
        us_show.tag_configure("center", justify='center',)
        us_show.tag_add("center", "1.0", "end")
        us_show.place(x=310, y=265)
        #add to list of screen contents
        self.play_screen_contents.append(us_show)

    def dealer_display_score(self):
        #show the card total for the dealer (minus the hold card)
        ds_show = tk.Text(height=1, width=20, fg="grey", bd=0,bg="darkgreen", font='Helvetica 12 bold')
        ds_show.insert(tk.END, f"Dealer Shows: {self.dealer_card_total_showing}")
        ds_show.tag_configure("center", justify='center')
        ds_show.tag_add("center", "1.0", "end")
        ds_show.place(x=310, y=215)
        #add to list of screen contents
        self.play_screen_contents.append(ds_show)

    def bet(self):
        #set pot amount and deduct from bank account
        self.pot=2*self.bet_amt
        self.bank_account-=self.bet_amt

    def make_hit_hold_buttons(self):
        #make Hit and Hold Buttons

        image = Image.open("./images/hit.png")
        i_width, i_height = image.size
        image = ImageTk.PhotoImage(image.resize((int(i_width//20), int(i_height//20)), Image.LANCZOS))
        hit_but = tk.Button(
            command=lambda: [self.user_hit(), self.kill_buy_ins_but()])
        hit_but.config(image=image, bg="darkgreen", bd=0)
        hit_but.image = image
        hit_but.place(x=175, y=325)

        image = Image.open("./images/stay.png")
        i_width, i_height = image.size
        image = ImageTk.PhotoImage(image.resize((int(i_width//20), int(i_height//20)), Image.LANCZOS))
        hold_but = tk.Button(
            command=lambda: [self.dealer_play(),self.kill_buy_ins_but()])
        hold_but.config(image=image, bg="darkgreen", bd=0)
        hold_but.image = image
        hold_but.place(x=325, y=325)

        image = Image.open("./images/dd.png")
        i_width, i_height = image.size
        image = ImageTk.PhotoImage(image.resize((int(i_width//3.25), int(i_height//3.25)), Image.LANCZOS))
        dd_but = tk.Button(
            command=lambda: [self.double_down(), self.kill_buy_ins_but()])
        dd_but.config(image=image, bg="darkgreen", bd=0)
        dd_but.image = image
        dd_but.place(x=475, y=325)

        if (self.insurance_offered and len(self.user_cards)==2):    
            image = Image.open("./images/gi.png")
            i_width, i_height = image.size
            image = ImageTk.PhotoImage(image.resize(
                (int(i_width//2), int(i_height//2)), Image.LANCZOS))
            bi_but = tk.Button(
                command=lambda: [self.buy_insurance(), self.kill_buy_ins_but(), self.check_for_blackjack()])
            bi_but.config(image=image, bg="white", bd=0)
            bi_but.image = image
            bi_but.place(x=620, y=335)
            self.insurance_button=bi_but


        self.play_screen_contents.append(hit_but)
        self.play_screen_contents.append(hold_but)
        self.play_screen_contents.append(dd_but)
        self.hhbut.append(hit_but)
        self.hhbut.append(hold_but)
        self.hhbut.append(dd_but)

    def kill_buy_ins_but(self):
        if(self.insurance_button):
            self.insurance_button.destroy()

    def buy_insurance(self):
        self.has_insurance=True
        self.bank_account-=self.bet_amt
        self.insurance_offered = False
        self.update_card_points_user()
        self.update_card_points_dealer()
        self.build_play_screen()

    def double_down(self):
        self.bank_account-=self.bet_amt
        self.pot*=2
        self.user_hit()
        self.dealer_play()

    def kill_hit_hold_buttons(self):
        for button in self.hhbut:
            button.destroy()

    def kill_betting_button(self):
        #removes the betting buttons from screen
        for button in self.betting_buttons:
            button.destroy()

    def make_betting_buttons(self):
        #betting function
        def change_bet(inc):
            if(self.bet_amt >= 1 and self.bet_amt+inc <= self.bank_account):
                self.bet_amt+=inc
            self.make_betting_buttons()

        #Adds the bet, increase bet 1/10, dec bet, and Check buttons:
        image = Image.open('./images/bet1.png')
        i_width, i_height = image.size        
        image = ImageTk.PhotoImage(image.resize((i_width//6, i_height//6), Image.LANCZOS))
        add_one_but = tk.Button(command=lambda: [change_bet(1)])
        add_one_but.config(image=image, bg="darkgreen", bd=0)
        add_one_but.image = image
        add_one_but.place(x=190, y=300)

        image = Image.open("./images/bet2.png")
        i_width, i_height = image.size
        image = ImageTk.PhotoImage(image.resize((i_width//6, i_height//6), Image.LANCZOS))
        add_ten_but = tk.Button(command=lambda: [change_bet(10)])
        add_ten_but.config(image=image, bg="darkgreen", bd=0)
        add_ten_but.image = image
        add_ten_but.place(x=300, y=300)

        image = Image.open("./images/placebet.png")
        i_width, i_height = image.size
        image = ImageTk.PhotoImage(image.resize((int(i_width//14.5), int(i_height//14.5)), Image.LANCZOS))
        bet_but = tk.Button(command=lambda: [self.bet(), self.start_dealing()])
        bet_but.config(image=image, bg="darkgreen", bd=0)
        bet_but.image = image
        bet_but.place(x=410, y=300)

        image = Image.open("./images/lowerbet.png")
        i_width, i_height = image.size
        image = ImageTk.PhotoImage(image.resize((int(i_width//11.25), int(i_height//11.25)), Image.LANCZOS))
        dec_bet_but = tk.Button(command=lambda: [change_bet(-1)])
        dec_bet_but.config(image=image, bg="darkgreen", bd=0)
        dec_bet_but.image = image
        dec_bet_but.place(x=520, y=300)

        bet_amt_txt = tk.Text(height=1, width=20, fg="white", bg="darkgreen", bd=0, font='Helvetica 16 bold')
        bet_amt_txt.insert(tk.END, f"Current Bet: {self.bet_amt}")
        bet_amt_txt.tag_configure("center", justify='center')
        bet_amt_txt.tag_add("center", "1.0", "end")
        bet_amt_txt.place(x=280, y=420)
        #add all buttons to items on screen
        self.betting_buttons.append(add_one_but)
        self.betting_buttons.append(add_ten_but)
        self.betting_buttons.append(bet_but)
        self.betting_buttons.append(dec_bet_but)
        self.betting_buttons.append(bet_amt_txt)

    def show_bank_account(self):
        #Shows bank account
        sba = tk.Text(height=3, width=10, fg="black",
                      bg="darkgreen", font='Helvetica 12 bold', bd=0)
        sba.insert(tk.END, f"Your Bank\nBalance is\n${int(self.bank_account)}")
        sba.tag_configure("center", justify='center')
        sba.tag_add("center", "1.0", "end")
        sba.place(x=200, y=220)
        self.play_screen_contents.append(sba)

    def show_pot(self):
        #Adds the Pot Total to center of screen x and higher on y
        pot = tk.Text(height=1, width=20, fg="white", bg="darkgreen", bd=0, font='Helvetica 12 bold')
        pot.insert(tk.END, f"Total Pot: ${int(self.pot)}")
        pot.tag_configure("center", justify='center')
        pot.tag_add("center", "1.0", "end")
        pot.place(x=310, y=240)
        self.play_screen_contents.append(pot)

    def show_last_hand_result(self):
        #get string to say you won or loss
        result_word=''
        if(self.last_game_won):
            result_word='Won'
        elif(self.last_game_push):
            result_word='Tied'
        else:
            result_word='Lost'    
        #Shows Results of previous hand
        slhr = tk.Text(height=4, width=13, fg="black",
                       bg="darkgreen", font='Helvetica 12 bold', bd=0)
        slhr.insert(tk.END, f"Last Hand\nYou {result_word}\nYour Earnings: \n${int(self.last_game_winnings)}")
        slhr.tag_configure("center", justify='center')
        slhr.tag_add("center", "1.0", "end")
        slhr.place(x=510, y=210)
        self.play_screen_contents.append(slhr)

    def build_initial_screen(self):
        #builds the betting screen
        self.show_pot()
        self.make_betting_buttons()
        self.dealer_display_score()
        self.user_display_score()
        self.show_last_hand_result()
        self.show_bank_account()

    def build_play_screen(self):
        #builds the screen that the cards are dealt on
        self.show_pot()
        self.make_hit_hold_buttons()
        self.dealer_display_score()
        self.user_display_score()
        self.show_last_hand_result()
        self.show_bank_account()
        
    def init_game(self):
        #starts the blackJack match after new game/restore screen
        self.kill_ngr()
        self.build_initial_screen()
        self.make_deck()

    def initUI(self):
        #makes window and starts teh game process
        self.master.title("Kevin's No Limit 5-Deck Black Jack")
        self.master.geometry("800x600+450+150")
        self.new_game_or_restore()

def main():
    root = Tk()
    root.configure(background="darkgreen")
    app = BlackJack(root)
    root.mainloop()

def refresh(root):
    root.destroy()
    main()

def restore(self):
    #restores the last game info and bank account from last session
    if path.isfile("saveblkjack.json"):
        with open("saveblkjack.json", "r") as save_file:
            data = json.load(save_file)
            self.bank_account = data[0]
            self.last_game_pot = data[1]
            self.last_game_won = data[2]
            self.last_game_winnings= data[3]
            self.last_game_push = data[4]
            self.deck=data[5]
        pass

def save(self):
    #saves the listed varibles amount
    save_data=[self.bank_account,self.last_game_pot,self.last_game_won,self.last_game_winnings,self.last_game_push,self.deck]
    with open("saveblkjack.json", "w") as save_file:
        json.dump(save_data, save_file)

if __name__ == '__main__':
    main()
