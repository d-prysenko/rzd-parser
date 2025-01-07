# Фильтры

## Фильтры для билетов

### OfferFilter
	Base Abstract Offer Filter
---
### OnlyLowerPlacesFilter
	Только нижние места
---
### PriceFilter
	Цена
#### Параметры:  
>**price**: float  
---
### WithPetsFilter
	Проезд с животными
---
## Фильтры для поездов

### DepartureTimeFilter
	Время выезда
#### Параметры:  
>**time_from**: str  
>**time_to**: str *= 23:59*  
---
### TrainFilter
	Base Abstract Train Filter
---
### TrainNumberEqual
	Номер поезда равен
#### Параметры:  
>**train_number**: str  
---
### TrainNumberNotEqual
	Номер поезда не равен
#### Параметры:  
>**train_number**: str  
---
### TripDurationLowerThan
	Время поездки
#### Параметры:  
>**minutes**: float  
---
