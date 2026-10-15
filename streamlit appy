import streamlit as st
import random

# --- Config ---
MAP_SIZE = 10
WALL_PROB = 0.12
NUM_ENEMIES = 8
NUM_TREASURES = 6

# --- Helpers ---
def make_empty_map(size, wall_prob):
    grid = []
    for y in range(size):
        row = []
        for x in range(size):
            if random.random() < wall_prob:
                row.append("#")  # wall
            else:
                row.append(".")  # floor
        grid.append(row)
    return grid

def place_item(grid, symbol):
    size = len(grid)
    while True:
        x = random.randrange(size)
        y = random.randrange(size)
        if grid[y][x] == ".":
            grid[y][x] = symbol
            return (x, y)

def pos_to_key(pos):
    return f"{pos[0]}_{pos[1]}"

def render_grid(grid, player_pos, enemies, treasures, exit_pos):
    # Emoji mapping
    emap = {
        "#": "⬛",  # wall
        ".": "⬜",  # floor
    }
    px, py = player_pos
    lines = []
    for y, row in enumerate(grid):
        line = ""
        for x, cell in enumerate(row):
            if (x, y) == (px, py):
                line += "🧑‍🚀"
            elif (x, y) in enemies:
                line += "👾"
            elif (x, y) in treasures:
                line += "💎"
            elif (x, y) == exit_pos:
                line += "🚪"
            else:
                line += emap.get(cell, "⬜")
        lines.append(line)
    return "\n".join(lines)

def init_game():
    grid = make_empty_map(MAP_SIZE, WALL_PROB)
    # ensure start and center exit are floors
    start = (0, 0)
    grid[start[1]][start[0]] = "."
    exit_pos = place_item(grid, ".")  # place exit on a floor (we'll keep its marker separately)
    # place enemies and treasures
    enemies = {}
    for _ in range(NUM_ENEMIES):
        pos = place_item(grid, ".")
        enemies[pos] = {"hp": random.randint(3, 7)}
    treasures = set()
    for _ in range(NUM_TREASURES):
        pos = place_item(grid, ".")
        treasures.add(pos)
    # place exit somewhere non-start
    while exit_pos == start:
        exit_pos = place_item(grid, ".")
    st.session_state.grid = grid
    st.session_state.player_pos = start
    st.session_state.hp = 15
    st.session_state.gold = 0
    st.session_state.enemies = enemies
    st.session_state.treasures = treasures
    st.session_state.exit_pos = exit_pos
    st.session_state.messages = ["Game bắt đầu! Tìm đường đến 🚪."]
    st.session_state.turn = 0

def move(dx, dy):
    px, py = st.session_state.player_pos
    nx, ny = px + dx, py + dy
    size = len(st.session_state.grid)
    if not (0 <= nx < size and 0 <= ny < size):
        st.session_state.messages.insert(0, "Không thể đi qua biên giới.")
        return
    if st.session_state.grid[ny][nx] == "#":
        st.session_state.messages.insert(0, "Có tường chắn ở đó.")
        return
    target = (nx, ny)
    # combat if enemy present
    if target in st.session_state.enemies:
        enemy = st.session_state.enemies[target]
        # simple exchange of hits
        player_attack = random.randint(1, 6)
        enemy['hp'] -= player_attack
        st.session_state.messages.insert(0, f"Bạn tấn công kẻ địch tại {target} gây {player_attack} sát thương.")
        if enemy['hp'] <= 0:
            del st.session_state.enemies[target]
            loot = random.randint(1, 5)
            st.session_state.gold += loot
            st.session_state.messages.insert(0, f"Bạn tiêu diệt kẻ địch! Nhặt được {loot} vàng.")
            # move into the cell
            st.session_state.player_pos = target
        else:
            enemy_attack = random.randint(1, 4)
            st.session_state.hp -= enemy_attack
            st.session_state.messages.insert(0, f"Kẻ địch phản công gây {enemy_attack} sát thương. HP còn {st.session_state.hp}.")
            if st.session_state.hp <= 0:
                st.session_state.messages.insert(0, "Bạn đã chết. Game over.")
    else:
        # move, pick treasure, check exit
        st.session_state.player_pos = target
        if target in st.session_state.treasures:
            gained = random.randint(5, 15)
            st.session_state.gold += gained
            st.session_state.treasures.remove(target)
            st.session_state.messages.insert(0, f"Bạn tìm thấy kho báu! +{gained} vàng.")
        if target == st.session_state.exit_pos:
            st.session_state.messages.insert(0, "Bạn đến cửa thoát! Bạn chiến thắng 🎉")
    st.session_state.turn += 1

# --- Page start ---
st.title("Mini Dungeon trên Streamlit")

if "grid" not in st.session_state:
    init_game()

# Top info
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.subheader("Trạng thái")
    st.write(f"HP: **{st.session_state.hp}**")
    st.write(f"Vàng: **{st.session_state.gold}**")
    st.write(f"Lượt: **{st.session_state.turn}**")
with col2:
    st.subheader("Quái vật")
    st.write(len(st.session_state.enemies))
with col3:
    st.subheader("Kho báu")
    st.write(len(st.session_state.treasures))

# Map
st.subheader("Bản đồ")
st.markdown(render_grid(st.session_state.grid, st.session_state.player_pos,
                        st.session_state.enemies, st.session_state.treasures,
                        st.session_state.exit_pos))

# Controls
st.subheader("Di chuyển")
c1, c2, c3 = st.columns([1,2,1])
with c1:
    if st.button("⬆️"):
        move(0, -1)
with c2:
    left, right = st.columns(2)
    with left:
        if st.button("⬅️"):
            move(-1, 0)
    with right:
        if st.button("➡️"):
            move(1, 0)
with c3:
    if st.button("⬇️"):
        move(0, 1)

# Actions
if st.button("Chờ (skip)"):
    st.session_state.messages.insert(0, "Bạn chờ một lượt...")
    st.session_state.turn += 1

if st.button("Khởi động lại"):
    init_game()
    st.experimental_rerun()

# Messages (recent)
st.subheader("Thông báo")
for m in st.session_state.messages[:10]:
    st.write("- " + m)

# Check player death or win and show restart suggestion
if st.session_state.hp <= 0:
    st.error("Bạn đã chết — nhấn 'Khởi động lại' để chơi lại.")
elif st.session_state.player_pos == st.session_state.exit_pos:
    st.success("Bạn đã thoát khỏi hầm ngục! Chúc mừng 🎉")
