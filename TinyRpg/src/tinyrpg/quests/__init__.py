from tinyrpg.engine.game.quest import Quest
from tinyrpg.quests.grace_quest import GraceQuest as GraceQuest
from tinyrpg.quests.grace_shop import GraceShop

QUESTS: dict[str, Quest] = {
    "grace_quest": GraceQuest(),
    "grace_shop": GraceShop(),
}
