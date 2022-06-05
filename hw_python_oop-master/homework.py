from dataclasses import dataclass,asdict

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    def show_training_info(self):
        return self.get_message
    def get_message(self):
        info_data=asdict(self)
        return (f"Тип тренировки: {info_data['training_type']}; Длительность: {info_data['duration']:.3f}"
            f" ч.; Дистанция: {info_data['distance']:.3f}  км;"
            f"Ср. скорость: {info_data['speed']:.3f} км/ч;"
            f"Потрачено ккал: {info_data['calories']:.3f}"
            )
            

class Training:
    """Базовый класс тренировки."""
    LEN_STEP=0.65
    M_IN_KM=1000
    MIN_IN_HOUR=60
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ):
        self.action=action
        self.duration=duration
        self.weight=weight
    

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        new_distance=self.action*self.LEN_STEP/self.M_IN_KM
        return new_distance
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        avg_speed=self.get_distance()/self.duration
        return avg_speed
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass
    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__, self.duration, self.get_distance(), self.get_mean_speed(), self.get_spent_calories()
        )
        


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1=18
    coeff_calorie_2=20

    def __init__(self, action: int, duration: float, weight: float):
        super().__init__(action, duration, weight)
    def get_spent_calories(self):
        return (
            (self.COEFF_CALORIE_1*self.get_mean_speed-self.coeff_calorie_2)*
            self.weight/self.M_IN_KM*self.duration*self.MIN_IN_HOUR
        )



class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_1=0.035
    coeff_calorie_2=0.029
    def __init__(self ,action, duration, weight, height):
        self.height=height
        super().__init__(action,duration,weight)
    def get_spent_calories(self):
        return (
            (self.coeff_calorie_1*self.weight+(self.get_mean_speed()**2//self.height)*self.coeff_calorie_2*
            self.weight)*self.duration*self.MIN_IN_HOUR
        )
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP=1.38
    coeff_calorie_1=1.1
    coeff_calorie_2=2
    def __init__(self,action,duration,weight,length_pool,count_pool):
        super().__init__(action,duration,weight)
        self.length_pool=length_pool
        self.count_pool=count_pool

    def get_spent_calories(self):
            return(
                (self.get_mean_speed+self.coeff_calorie_1)*self.coeff_calorie_2*self.weight
            )
    def get_mean_speed(self):
        avg_speed=self.length_pool*self.count_pool/self.M_IN_KM/self.duration



def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    read_tr_data={'SWM':Swimming,'RUN':Running, 'WLK':SportsWalking}
    try: return read_tr_data[workout_type](*data)
    except KeyError:
        raise KeyError('Ошибка')


def main(training: Training) -> None:
    """Главная функция."""
    info=training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
