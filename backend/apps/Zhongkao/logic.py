import random
async def handle_genScore():
    # Fake response for now - returns fixed scores
    fake_scores = [100, 95, 88, 60, 45, 50, 16, 12, 16, 12]
    
    return {
        "scores": [random.randint(115, 130),
                   random.randint(110, 125),
                   random.randint(125, 140),
                   random.randint(58, 69),
                   random.randint(39, 49),
                   random.randint(50, 60),
                   random.choice([20, 16]),
                   random.choice([20, 16]),
                   random.choice([20, 16]),
                   random.choice([20, 16])
                   ]
    }    