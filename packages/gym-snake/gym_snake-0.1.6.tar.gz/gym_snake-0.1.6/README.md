# Snake for gym

Среда сделана в формате [gym](https://gym.openai.com)

**Правила игры**

Игровое поле 20x20, В начале игрового эпизода змея и яблока располагаются случайно, змея состоит из одной клетки - головы.
Змея может двигаться во всех 4-х направлениях кроме назад (в себя). Яблоко неподвижно на протяжении эпизода. При поедании яблока длина змеи увеличивается на одну клетку.

Действия:

0 - left, 1 - up, 2 - right, 3 - down.

Эпизод состоит из не более 200 шагов. 

Награды (reward):
- за правильный, но нерезультативный код: -1
- за неправильный ход (в себя или за пределы поля): -100 и эпизод завершается.
- за яблоко: +100

Задача - набрать максимальное число очков за эпизод.

**Как запустить игру**

Для начала нужно установить пакет gym_snake

Склонируйте репозиторий

```
git clone https://github.com/boangri/gym-snake.git
pip install -e gym-snake
```

Пример случайного агента:

```
import gym
import gym_snake

env = gym.make('Snake-v0')
observation = env.reset()
done = False
score = 0
steps = 0
while not done:
    env.render()
    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)
    score += reward
    steps += 1
    print("step %d action %d => %d, total: %d" % (steps, action, reward, score))
print("End of episode")
```
