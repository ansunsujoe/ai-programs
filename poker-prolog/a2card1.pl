%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  Ansun Sujoe - AXS180210
%%  a2card1.pl
%%  Three card poker
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% -----------------------------------
%% Simulate poker for two players
%% -----------------------------------
simulate2p :-
  Grid = [[0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]],
  playturns(100000,Grid).

%%  Playing the game for iterations
playturns(0, Grid) :-
  nl,
  write('Grid:'),
  nl,
  print2pGrid(Grid).

playturns(X, Grid) :-
  play2(I, J), 
  nth0(I, Grid, L),
  nth0(J, L, N),
  N1 is N + 1,
  replace(L, J, N1, NRow),
  replace(Grid, I, NRow, Grid1),
  S is X - 1,
  playturns(S, Grid1), !.

% Replace one grid row
replace([_|T], 0, X, [X|T]).
replace([H|T], I, X, [H|R]) :- 
  I > -1, 
  NI is I-1, 
  replace(T, NI, X, R), !.
replace(L, _, _, L).

% Print a grid in nice format
print2pGrid([]).
print2pGrid([X|R]) :-
  format('~w\t~w\t~w\t~w\t~w\t~w\t~w\t~w\t~w\t~w\t~n',X),
  print2pGrid(R).

%% -----------------------------------
%% Simulate poker for 1 player - probabilities
%% -----------------------------------
simulate1p :-
  Freq = [0,0,0,0,0,0],
  write('Dealing 10,000 hands... '), nl,
  play1pIteration(10000, Freq).

probabilityDivide(X, Y) :-
  Y is X / 10000.

play1pIteration(0, Freq) :-
  nl,
  write('Frequencies:'),
  nl,
  print(Freq),
  nl,
  write('Probabilities:'),
  nl,
  maplist(probabilityDivide, Freq, Probs),
  print(Probs).

play1pIteration(N, Freq) :-
  play1p(I),
  nth0(I, Freq, Old),
  New is Old + 1,
  replace(Freq, I, New, Freq1),
  S is N - 1,
  play1pIteration(S, Freq1), !.

%% -----------------------------------
%% Play2 for one deal with 2 players
%% -----------------------------------

% play2(I, J) :- 
%   deal(3,H1,H2),
%   winner(H1,H2, Winner),
%   nl, write('Player 1 has '), sort_hand(H1, Sorted_Hand1),
%   determine_hand(Sorted_Hand1, X), rank(X, I), print(X), write(', Rank: '), print(I), 
%   write(', Hand: '), print(Sorted_Hand1), nl, write('Player 2 has '), sort_hand(H2, Sorted_Hand2),
%   determine_hand(Sorted_Hand2, Y), rank(Y, J), print(Y), write(', Rank: '), print(J), 
%   write(', Hand: '), print(Sorted_Hand2), nl,
%   write('Winner is Player '), print(Winner),nl.

play2(I, J) :- 
  deal(3,H1,H2), !,
  winner(H1,H2, Winner), sort_hand(H1, Sorted_Hand1),
  determine_hand(Sorted_Hand1, X), rank(X, I), sort_hand(H2, Sorted_Hand2),
  determine_hand(Sorted_Hand2, Y), rank(Y, J).


play([],0).
play([[Hand1,Hand2]|Rst], Num_Wins) :-
  winner(Hand1, Hand2, Winner),
  (Winner = Hand1, play(Rst,Remaining), Num_Wins is 1 + Remaining ;
   play(Rst, Num_Wins)).

%% -----------------------------------
%% Play2 for one deal with 1 player
%% -----------------------------------

% play1p(I) :-
%   deal1p(3,H),
%   sort_hand(H, Sorted_Hand),
%   determine_hand(Sorted_Hand, X),
%   rank(X, I),
%   write('Hand: '), print(Sorted_Hand), nl,
%   write('Rank: '), print(I), nl, nl, !.

play1p(I) :- 
  deal1p(3,H),
  sort_hand(H, Sorted_Hand),
  determine_hand(Sorted_Hand, X),
  rank(X, I), !.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  Playing the game.
winner(H1, H2, Winner) :-
  sort_hand(H1, Sorted_Hand1),
  sort_hand(H2, Sorted_Hand2),
  determine_hand(Sorted_Hand1,  X1),
  determine_hand(Sorted_Hand2,  X2),
  beats(X1, X2, Verdict),
  (Verdict = X1, Winner = H1;
   Verdict = X2, Winner = H2;
   Verdict = tie, tiebreak(X1, Sorted_Hand1, Sorted_Hand2, SortedWinner),
   (SortedWinner = left, Winner = H1 ;
    SortedWinner = right, Winner = H2)), !.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Generate Random Hand
randomHand(0, _, [], []).

randomHand(N, Deck, [X|NextXSelections], [Y|NextYSelections]) :-
  random_member(X, Deck),
  select(X, Deck, R),
  random_member(Y, R),
  select(Y, R, S),
  N1 is N - 1,
  randomHand(N1, S, NextXSelections, NextYSelections), !.

%% Generate Random Hand for 1 person
randomHand1(0, _, []).

randomHand1(N, Deck, [X|NextXSelections]) :-
  random_member(X, Deck),
  select(X, Deck, R),
  N1 is N - 1,
  randomHand1(N1, R, NextXSelections), !.

deal(N, X, Y) :-
  D = [[2,spade],[3,spade],[4,spade],[5,spade],[6,spade],[7,spade],[8,spade],
  [9,spade],[10,spade],[jack,spade],[queen,spade],[king,spade],[ace,spade],
  [2,diamond],[3,diamond],[4,diamond],[5,diamond],[6,diamond],[7,diamond],[8,diamond],
  [9,diamond],[10,diamond],[jack,diamond],[queen,diamond],[king,diamond],[ace,diamond],
  [2,club],[3,club],[4,club],[5,club],[6,club],[7,club],[8,club],
  [9,club],[10,club],[jack,club],[queen,club],[king,club],[ace,club],
  [2,heart],[3,heart],[4,heart],[5,heart],[6,heart],[7,heart],[8,heart],
  [9,heart],[10,heart],[jack,heart],[queen,heart],[king,heart],[ace,heart]],
  randomHand(N, D, X, Y), !.

deal1p(N, X) :-
  D = [[2,spade],[3,spade],[4,spade],[5,spade],[6,spade],[7,spade],[8,spade],
  [9,spade],[10,spade],[jack,spade],[queen,spade],[king,spade],[ace,spade],
  [2,diamond],[3,diamond],[4,diamond],[5,diamond],[6,diamond],[7,diamond],[8,diamond],
  [9,diamond],[10,diamond],[jack,diamond],[queen,diamond],[king,diamond],[ace,diamond],
  [2,club],[3,club],[4,club],[5,club],[6,club],[7,club],[8,club],
  [9,club],[10,club],[jack,club],[queen,club],[king,club],[ace,club],
  [2,heart],[3,heart],[4,heart],[5,heart],[6,heart],[7,heart],[8,heart],
  [9,heart],[10,heart],[jack,heart],[queen,heart],[king,heart],[ace,heart]],
  randomHand1(N, D, X), !.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Fill Table

ranklist(A, [A|_], 0).
ranklist(A, [X|Y], N) :-
  ranklist(A, Y, N1),
  N is N1 + 1.

rank(A, R) :-
  List = [straight_flush, three_of_a_kind, straight, flush, pair, high_card],
  ranklist(A, List, R), !.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  Tiebreaks
tiebreak(straight_flush, H1, H2, Winner)  :- higher_last_card(H1, H2, Winner).
tiebreak(flush, H1, H2, Winner)           :- tiebreak(high_card, H1, H2, Winner).
tiebreak(straight, H1, H2, Winner)        :- higher_last_card(H1, H2, Winner).
     
tiebreak(pair, H1, H2, Winner) :-
  isolate_pair(H1, [PairCard1,_], Rst1),
  isolate_pair(H2, [PairCard2,_], Rst2),
  (beats_with_hand(H1, PairCard1, H2, PairCard2, Winner), Winner \= tie ;
   tiebreak(high_card, Rst1, Rst2, Winner)).

tiebreak(high_card, H1, H2, X) :- 
  reverse(H1, RevH1),
  reverse(H2, RevH2),
  highest_card_chain(RevH1, RevH2, X).

beats_with_hand(H1, C1, H2, C2, X) :-
  beats(C1, C2, C1), X = left ;
  beats(C1, C2, C2), X = right ;
  X = tie.

isolate_pair(Hand, Pair, Rst) :-
  [[V1,S1],[V2,S2],[V3,S3]] = Hand,
  (V1 = V2, Pair = [[V1,S1],[V2,S2]], Rst = [[V3,S3]] ;
   V2 = V3, Pair = [[V3,S3],[V2,S2]], Rst = [[V1,S1]]).
  

highest_card_chain([H1|T1], [H2|T2], X) :-
  beats(H1,H2,Verdict),
  (Verdict = H1, X = left ;
   Verdict = H2, X = right ;
   Verdict = tie, highest_card_chain(T1,T2,X)).

higher_last_card(H1,H2,Winner) :-
  H1 = [_,_,[V1,_]],
  H2 = [_,_,[V2,_]],
  beats(V1,V2,Higher),
  (Higher = V1, Winner = left ;
   Higher = V2, Winner = right).

higher_middle_card(H1, H2, Winner) :-
  H1 = [_,[V1,_],_],
  H2 = [_,[V2,_],_],
  beats(V1,V2,Higher),
  (Higher = V1, Winner = left;
   Higher = V2, Winner = right).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  Hand determination

determine_hand([[A,X],[B,X],[C,X]], straight_flush) :-
  successor(C,B), successor(B,A).

determine_hand([[_,X],[_,X],[_,X]], flush).

determine_hand([[A,_],[B,_],[C,_]], straight) :-
  successor(C,B), successor(B,A).

determine_hand([[A,_],[B,_],[C,_]], three_of_a_kind) :-
  A = B,
  B = C.

determine_hand([[A,_],[B,_],[C,_]], pair) :-
  A = B; B = C.

determine_hand(_,high_card).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  Hand sorting (for easier pattern matching).
sort_hand([], []).
sort_hand([H|T], Sorted) :-
  filter_by_high_card(H,T,Lower,Higher),
  sort_hand(Lower,SortedLower),
  sort_hand(Higher,SortedHigher),
  append(SortedLower, [H|SortedHigher], Sorted).


filter_by_high_card(_, [], [], []).  
filter_by_high_card(Pivot, [H|T], [H|Lower], Higher) :-
  beats(Pivot,H,Z),
  (Z = Pivot ; Z = tie),
  filter_by_high_card(Pivot, T, Lower, Higher).
filter_by_high_card(Pivot, [H|T], Lower, [H|Higher]) :-
  beats(Pivot,H,H),
  filter_by_high_card(Pivot, T, Lower, Higher).


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  Card and Hand Precedence
beats([V,_],[V,_],tie).
beats([V1,S],[V2,_],[V1,S]) :- value_greater_than(V1,V2).
beats([V1,_],[V2,S],[V2,S]) :- value_greater_than(V2,V1).

beats(X,X,tie).
beats(X,Y,X) :- value_greater_than(X,Y).
beats(X,Y,Y) :- value_greater_than(Y,X).

successor(straight_flush, three_of_a_kind).      successor(three_of_a_kind, straight).
successor(straight, flush).     successor(flush, pair).
successor(pair, high_card).

successor(ace,king).     successor(king,queen).   successor(queen,jack).
successor(jack,10).      successor(10,9).         successor(9,8).
successor(8,7).          successor(7,6).          successor(6,5).
successor(5,4).          successor(4,3).          successor(3,2).

value_greater_than(X,Y) :-
  successor(X,P),
  (Y = P;
  value_greater_than(P,Y)).
