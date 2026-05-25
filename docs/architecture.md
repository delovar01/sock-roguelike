# Архитектура

## Общий обзор

Игра построена по MVC-подобному принципу с разделением на системы.
Формальных классов Model/View/Controller нет, но роли разнесены:

- **Model** — `src/entities/` + `src/world/`. Игрок, враги, предметы,
  уровень. Хранят состояние, не знают про экран и ввод.
- **View** — `src/systems/render_system.py` + `src/ui/`. Рисуют
  состояние модели на экран.
- **Controller** — `src/core/input_manager.py` + `src/systems/movement_system.py`
  + `src/systems/ai_system.py` + `src/systems/collision_system.py`.
  Меняют модель в ответ на ввод или ИИ.

Между системами связь идёт через шину событий
(`src/core/event_bus.py`, паттерн Observer): Player не знает, что
HUD и звуковая подсистема его слушают, и наоборот.

## Главный цикл

`Game` (`src/core/game.py`) — корневой объект. Внутри `run()`:

1. читаем `dt` от `clock.tick(FPS)`
2. обрабатываем события (`QUIT`, нажатия клавиш) — раздаём их активной
   сцене и `InputManager`
3. вызываем `scene.update(dt)` — там вся игровая логика
4. чистим экран, вызываем `scene.draw(surface)`
5. `pygame.display.flip()` — показываем кадр

Сцена меняется через `Game.change_scene(...)` — реально подменяется
после текущего тика, чтобы не сломать обход.

## Сцены

- `MenuScene` — главное меню, кнопки "Новая игра / Продолжить / Выход",
  показывает сюжетный текст из `assets/story/intro.txt`.
- `GameScene` — генерирует уровень через BSP, расставляет врагов и
  пуговицы, держит игровой цикл.
- `DeathScene` — экран смерти.
- `WinScene` — экран победы (после 3-го уровня).

Базовый класс `BaseScene` определяет три метода: `handle_event`,
`update`, `draw`. Каждый дочерний класс их переопределяет. Получается
узкий интерфейс — принцип Interface Segregation.

В `GameScene` есть встроенная пауза (Esc) с пунктами:
- Esc — продолжить
- Q — выйти в меню (с автосохранением)
- +/- — изменить громкость музыки

Это и есть «меню настроек» из методички.

## Сущности

Все игровые объекты — наследники `Entity` (`src/entities/entity.py`).
Хранят позицию в тайлах, не в пикселях, чтобы не зависеть от размера
тайла.

- `Player` — носок. `_hp` инкапсулирован (одно подчёркивание плюс
  `@property hp` без сеттера). Изменение HP только через `take_damage()`
  и `heal()`. Есть `attack_damage` — растёт от подобранных иголок.
- `Enemy` — моль. Хранит HP, состояние FSM, маршрут патруля и путь от A*.
- `Spider` — наследник `Enemy`. Быстрее, видит ближе, HP меньше. Хороший
  пример полиморфизма: в системах нигде нет `isinstance(enemy, Spider)`.
- `Item` — базовый класс. У каждого подкласса свой `on_pickup(player)`:
  - `Button` (пуговица) — `player.heal(1)`
  - `Needle` (иголка) — `player.add_attack(1)`

## Системы

Каждая система отвечает только за одно (принцип Single Responsibility):

- `MovementSystem` — двигает игрока и врагов на одну клетку,
  с проверкой `Level.is_walkable`.
- `CollisionSystem` — AABB, проверяет пересечения игрока с предметами
  и врагами. Метод `player_attack` бьёт в 4 соседние клетки. При
  подборе, смерти, ударе и убийстве — эмитит события.
- `AISystem` — обновляет FSM врагов, при состоянии Chase вызывает
  поисковик пути (зависит от абстракции через параметр конструктора —
  принцип Dependency Inversion).
- `RenderSystem` — рисует уровень и сущности, есть debug-режим.

## Соответствие SOLID

| Принцип | Где |
|---|---|
| Single Responsibility | системы по одной отвечают за свою задачу |
| Open/Closed | новый тип врага = подкласс `Enemy`, системы не меняются |
| Liskov | `MovementSystem` работает с `Player` и `Enemy` одинаково |
| Interface Segregation | `BaseScene` — три метода, не больше |
| Dependency Inversion | `AISystem` принимает поисковик пути как параметр |

## Структура папок

```
src/
  core/         constants, game, event_bus, input_manager, resource_manager
  scenes/       base_scene, menu_scene, game_scene, death_scene, win_scene
  entities/     entity, player, enemy, item
  systems/      movement, collision, ai, render
  algorithms/   bsp_dungeon, a_star
  world/        tile, level, camera
  ui/           menu, hud
  persistence/  save_manager (JSON)
```

См. также `docs/algorithms.md` про конкретные алгоритмы.
