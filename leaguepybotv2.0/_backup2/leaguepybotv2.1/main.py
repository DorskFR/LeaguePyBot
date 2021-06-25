-> Bot
    -> Client ?
    -> WebSocket
        -> Observer("champ_selection", objects)
            -> call execute() on all objects
        -> Observer("match_making_accept", objects)
            -> call execute() on all objects
        -> Observer("game_flow", objects)
            -> call execute() on all objects




    function pick_champ:
        -> create PickChampion object
        -> Register to Observer "champ_selection"
    
    function ban_champ:
        -> Create BanChampion object
        -> Register to Observer "champ_selection"

    function create_match(Match type):
        -> Create RankedMatch object
        -> Create ChooseRole object
        -> function startMatch