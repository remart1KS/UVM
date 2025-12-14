; Корректная тестовая программа
; Записываем значения
load_const 10
load_const 100
write_value

load_const 20
load_const 200
write_value

; Читаем значение
load_const 10
read_value 0

; Bitreverse
load_const 10
bitreverse 5