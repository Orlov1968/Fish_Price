import os
import pandas as pd


class PriceMachine:

    def __init__(self):
        self.prices = pd.DataFrame(columns=['№', 'Наименование', 'Цена', 'Вес', 'Цена за кг.', 'Файл'])

    def load_prices(self, file_path=os.path.dirname(os.path.realpath(__file__))):

        for file in os.listdir(file_path):
            if file.endswith('.csv') and 'price' in file:
                df = pd.read_csv(os.path.join(file_path, file), encoding='utf-8')
                # Форматирую файлы согласно условию
                new_df = self._search_product_price_weight(df)
                # добавляю столбец с названием файла
                new_df['Файл'] = file.split('.')[0]
                # объединяю в один Data Frame
                self.prices = pd.concat([self.prices, new_df])
        # Создаю столбец цена за 1 кг.
        self.prices['Цена за кг.'] = self.prices['Цена'] / self.prices['Вес']
        # Сортирую по столбцу 'Цена за кг.'
        self.prices.sort_values(by='Цена за кг.', ascending=True, inplace=True)
        self.prices['№'] = range(1, len(self.prices) + 1)
        return self.prices

    def _search_product_price_weight(self, dt_frame):
        dt_frame = dt_frame.dropna(how="all", axis=1)
        for i, header in enumerate(dt_frame):
            if header.lower() in ['название', 'продукт', 'товар', 'наименование']:
                dt_frame = dt_frame.rename(columns={header: 'Наименование'})
            elif header.lower() in ['цена', 'розница']:
                dt_frame = dt_frame.rename(columns={header: 'Цена'})
            elif header.lower() in ['вес', 'масса', 'фасовка']:
                dt_frame = dt_frame.rename(columns={header: 'Вес'})
            else:
                dt_frame = dt_frame.drop(columns=[header])
        return dt_frame

    def export_to_html(self, df, file_name='output.html'):
        """
        Заполняем таблицу в HTML документе
        и сохраняем в файл
        :param df:
        :param file_name
        :return:
        """
        result = '''<!DOCTYPE html>
            <html>
            <head>
                <title>Позиции продуктов</title>
                    <style>
                        table {
                            border-spacing: 16px 0px; /* Расстояние между ячейками */ 
                        }
                    </style>
            </head>
            <body>
                <table>
                    <tr>
                        <th>Номер</th>
                        <th>Название</th>
                        <th>Цена</th>
                        <th>Фасовка</th>
                        <th>Файл</th>
                        <th>Цена за кг.</th>
                    </tr>
            '''
        for i in range(len(df)):
            result += '<tr>'
            result += f'<td align="right"> {df["№"].values[i]}</td>'
            result += f'<td> {df["Наименование"].values[i]}</td>'
            result += f'<td align="right"> {df["Цена"].values[i]}</td>'
            result += f'<td align="right"> {df["Вес"].values[i]}</td>'
            result += f'<td> {df["Файл"].values[i]}</td>'
            result += f'<td align="right"> {round(df["Цена за кг."].values[i], 1)}</td>'
            result += '</tr>\n'
        result += '\t</table>\n'
        result += '</body>'
        with open(file_name, 'w') as f:
            f.write(result)

    def find_text(self, search_text):
        """
        Поиск данных в получившемся дата-фрейме и вывод на консоль
        если данных по запросу не нашлось - выводим запрос по умолчанию
        для примера (и для проверок при написании этой программы)
        :param search_text:
        :return:
        """
        matches = self.prices[self.prices['Наименование'].str.contains(search_text, case=False)]
        if len(matches):
            self.export_to_html(df=matches, file_name='output.html')
            return matches
        else:
            print(f'Продукта с наименованием: {search_text}, не найдено. ')


if __name__ == "__main__":
    pm = PriceMachine()
    pm.load_prices()
    pm.export_to_html(file_name='output.html', df=pm.find_text(''))
    print('Команда - "exit" - завершить работу программы')
    while True:
        search_text = input('Введите наименование продукта: ')
        if search_text.lower().strip() == "exit":
            break
        elif search_text == "all":
            print(pm.prices)
        else:
            print(pm.find_text(search_text))
    print('Работа завершена.')
