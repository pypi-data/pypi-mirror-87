# /usr/bin/python3
# -*- coding: utf-8 -*-
""" unit tests """
import sys
import os
import pytest
import collections

# особенность работы с pytest :)
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from .. import business_scenarios


class TestBusinessLogic:
    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_unauthorized_access(self):
        sc = business_scenarios.BusinessLogic(login="ksavinov", url="http://orange.polymatica.ru:480", jupiter=True)
        sc.logout()
        res = sc.get_cube(cube_name="mee ИП в отношении ЮЛ (+Регион ОСП)")
        assert "Only authentication command allowed" in res

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_business_scenario1(self):
        # Авторизация
        sc = business_scenarios.BusinessLogic(login="ksavinov", url="http://orange.polymatica.ru:480", jupiter=True)
        # 6.1. Открыть мультисферу «mee ИП в отношении ЮЛ (+Регион ОСП)»
        sc.get_cube(cube_name="mee ИП в отношении ЮЛ (+Регион ОСП)")
        # 6.2. Вынести размерность Федеральный округ ОСП
        sc.move_dimension(dim_name="Федеральный округ ОСП", position="left", level=0)
        # 6.3. Убрать в фильтре размерности Федеральный округ ОСП элемент «Пустой»
        sc.delete_dim_filter(dim_name="Федеральный округ ОСП", filter_name="(Пустой)")
        # 6.4. Вынести правее размерность Должник
        sc.move_dimension(dim_name="Должник", position="left", level=1)
        # 6.5. Вынести правее размерность Номер ИП
        sc.move_dimension(dim_name="Номер ИП", position="left", level=2)
        # 6.6. Выбрать в фильтре размерности Предмет исполнения элемент «Оплата труда и иные выплаты по трудовым правоотношениям»
        sc.clear_all_dim_filters(dim_name="Предмет исполнения")
        sc.put_dim_filter(dim_name="Предмет исполнения",
                          filter_name="Оплата труда и иные выплаты по трудовым правоотношениям")
        # 6.7. Создать составную размерность Дата возбуждения год*Дата возбуждения месяц и переименовать на Дата возбуждения год-месяц
        sc.create_consistent_dim(formula="[Дата возбуждения год]*[Дата возбуждения месяц]", separator="*",
                                 dimension_list=["Дата возбуждения год", "Дата возбуждения месяц"])
        # 6.8. Выбрать в фильтре размерности Дата возбуждения год-месяц элементы «2020*Январь», «2020*Февраль»
        sc.put_dim_filter(dim_name="[Дата возбуждения год]*[Дата возбуждения месяц]",
                          filter_name=["2020*Январь", "2020*Февраль"])
        # 6.9. Включить фильтр по неактивным размерностям
        sc.switch_unactive_dims_filter()
        # 6.10. Создать копию факта Сумма долга
        sum_copy_fact_id = sc.copy_measure(measure_name="Сумма долга")
        # 6.11. Переименовать факт Копия 1 Сумма долга на Кол-во должников
        sc.rename_measure(measure_name="Копия 1 Сумма долга", new_measure_name="Кол-во должников")
        # 6.12. Поменять вид факта Кол-во должников на «Количество»
        sc.change_measure_type(measure_id=sum_copy_fact_id, type_name="Количество")
        # 6.13. Создать копию факта Сумма долга
        new_sum_copy_fact_id = sc.copy_measure("Сумма долга")
        # 6.14. Переименовать факт Копия 2 Сумма долга на Кол-во возбужденных ИП
        sc.rename_measure(measure_name="Копия 1 Сумма долга", new_measure_name="Кол-во возбужденных ИП")
        # 6.15. Поменять вид факта Кол-во возбужденных ИП на «Количество»
        sc.change_measure_type(measure_id=new_sum_copy_fact_id, type_name="Количество")
        # 6.16. Поменять уровень расчета факта Кол-во возбужденных ИП на 2-й
        sc.set_measure_level(measure_name="Кол-во возбужденных ИП", level=2)
        # 6.17. Поменять в формате факта Кол-во должников точность на 0
        # 6.18. Поменять в формате факта Кол-во возбужденных ИП точность на 0
        sc.set_measure_precision(measure_names=["Кол-во должников", "Кол-во возбужденных ИП"], precision=[0, 0])
        # 6.19. Создать вычислимый факт Погашенная задолженность с формулой
        sc.create_calculated_measure(new_name="Погашенная задолженность", formula="[Сумма долга] + 100")
        # 6.20. Выставить факты в следующем порядке:
        #     ▪ Кол-во должников
        #     ▪ Кол-во возбужденных ИП
        #     ▪ Сумма долга
        #     ▪ Погашенный долг
        #     ▪ Остаток долга
        sc.move_measures(new_order=["Кол-во должников", "Кол-во возбужденных ИП", "Сумма долга", "Остаток долга"])

        # получить DataFrame
        sc.get_data_frame()

        # завершить текущую сессию
        sc.logout()

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_formulas_in_calc_measure(self):
        sc = business_scenarios.BusinessLogic(login="ksavinov", url="http://orange.polymatica.ru:480", jupiter=True)
        sc.get_cube(cube_name="MedicineTest")
        # Создать вычислимые факты
        sc.create_calculated_measure(new_name="новая сумма долга", formula="top([Больница];1000)")
        sc.create_calculated_measure(new_name="очень сложные рассчеты",
                                     formula="100 + [Больница] / [Количество вызовов врача] * 2 + "
                                             "corr([Количество вызовов врача];[Больница])")
        sc.create_calculated_measure(new_name="прочие операнды",
                                     formula="[Больница] > 1 or [Больница] < 1 and [Больница] != 1000")
        # негативные случаи:
        try:
            sc.create_calculated_measure(new_name="странные символы",
                                         formula="[Больница] ** &?")
        except ValueError as e:
            assert "Unknown element in formula" in str(e)

        try:
            sc.create_calculated_measure(new_name="проблемы с балансом )))",
                                         formula="( ( [Больница] - [Количество вызовов врача] )")
        except ValueError as e:
            assert "Неправильный баланс скобочек в формуле" in str(e)
        sc.logout()

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_scenarios(self):
        sc = business_scenarios.BusinessLogic(login="ksavinov", url="http://orange.polymatica.ru:480", jupiter=True)
        sc.run_scenario(scenario_name="Вызовы и посещения 2018-2020")
        sc.move_dimension(dim_name="Год", position="left", level=0)
        sc.unfold_all_dims(position="left", level=0)
        sc.move_up_dims_to_left()
        my_layer = sc.active_layer_id
        layers_info = sc.execute_manager_command(command_name="user_layer", state="get_session_layers")
        assert my_layer in str(layers_info)
        sc.close_layer(sc.active_layer_id)
        layers_info = sc.execute_manager_command(command_name="user_layer", state="get_session_layers")
        assert my_layer not in str(layers_info)
        sc.logout()

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_permissions(self):
        # Под админом: авторизоваться
        sc = business_scenarios.BusinessLogic(login="ksavinov", url="http://orange.polymatica.ru:480", jupiter=True)

        # Под админом: дать пользователю user1 все роли и права
        sc.grant_permissions(user_name="ksavinov1")

        # проверка, что у пользователя все права
        result = sc.execute_manager_command(command_name="user", state="list_request")
        users_data = sc.h.parse_result(result=result, key="users")
        user_permissions = {k: v for data in users_data for k, v in data.items() if data["login"] == "ksavinov1"}
        requested_uuid = user_permissions["uuid"]
        # cubes permissions for user
        result = sc.execute_manager_command(command_name="user_cube", state="user_permissions_request",
                                            user_id=requested_uuid)
        users_data = sc.h.parse_result(result=result, key="permissions")
        assert False not in users_data

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_close_layer_after_getting_cube(self):
        sc = business_scenarios.BusinessLogic(login="ksavinov", url="http://orange.polymatica.ru:480", jupiter=True)
        # 6.1. Открыть мультисферу «mee ИП в отношении ЮЛ (+Регион ОСП)»
        sc.get_cube(cube_name="mee ИП в отношении ЮЛ (+Регион ОСП)")
        layers_info = sc.execute_manager_command(command_name="user_layer", state="get_session_layers")
        my_layer = sc.active_layer_id
        assert my_layer in str(layers_info)
        sc.close_layer(sc.active_layer_id)
        layers_info = sc.execute_manager_command(command_name="user_layer", state="get_session_layers")
        assert my_layer not in str(layers_info)
        sc.logout()

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_profiles(self):
        sc = business_scenarios.BusinessLogic(login="ksavinov", url="http://orange.polymatica.ru:480", jupiter=True)
        sc.load_profile(name="тестовое")
        sc.logout()

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_negative_profiles_scenarios(self):
        sc = business_scenarios.BusinessLogic(login="ksavinov", url="http://orange.polymatica.ru:480", jupiter=True)
        try:
            sc.load_profile(name="тестовое_fake")
        except ValueError as e:
            assert "No such profile" in str(e)
        try:
            sc.run_scenario(scenario_name="есть ли здесь такой сценарий?")
        except ValueError as e:
            assert "No such scenario" in str(e)
        sc.logout()

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_export(self):
        sc = business_scenarios.BusinessLogic(login="ksavinov", url="http://orange.polymatica.ru:480", jupiter=True)
        sc.get_cube(cube_name="mee ИП в отношении ЮЛ (+Регион ОСП)")
        sc.move_dimension(dim_name="Федеральный округ ОСП", position="left", level=0)

        csv_file, path = sc.export("D:\\polymatica\\polymatica\\tests", "csv")
        json_file = sc.export("D:\\polymatica\\polymatica\\tests", "json")
        json_file = json_file[0]
        xls_file = sc.export("D:\\polymatica\\polymatica\\tests", "xls")
        xls_file = xls_file[0]
        file_list = os.listdir(path)

        assert csv_file in file_list
        os.remove(path + "\\" + csv_file)
        assert json_file in file_list
        os.remove(path + "\\" + json_file)
        assert xls_file in file_list
        os.remove(path + "\\" + xls_file)

        sc.logout()

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_dims_facts_checks(self):
        sc = business_scenarios.BusinessLogic(login="ksavinov", url="http://orange.polymatica.ru:480", jupiter=True)
        sc.get_cube(cube_name="mee ИП в отношении ЮЛ (+Регион ОСП)")
        sc.move_dimension(dim_name="ОСП", position="left", level=0)

        measure_id = sc.get_measure_id(measure_name="Сумма долга")
        dim_id = sc.get_dim_id(dim_name="ОСП")

        dim_name = sc.get_dim_name(dim_id)
        measure_name = sc.get_measure_name(measure_id)

        assert dim_name == "ОСП"
        assert measure_name == "Сумма долга"

        sc.group_dimensions(["Балейский РОСП", "Бабушкинский ОСП"])

        sc.sort_measure("Сумма долга", "ascending")
        sc.sort_measure("Остаток долга", "descending")

        result = sc.set_measure_visibility(measure_name)

        assert measure_id in result, "Measure_id: %s measure_list: %s" % (measure_id, result)

        result = sc.execute_olap_command(command_name="fact", state="list_rq")

        facts_lst = sc.h.parse_result(result=result, key="facts")

        for elem in facts_lst:
            if elem["name"] == measure_name:
                assert elem["visible"] is False, elem
                
        sc.rename_dimension(dim_name="ОСП", new_name="новая размерность")
                
        sc.select_all_dims()

        sc.logout()

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_clone_multisphere(self):
        sc = business_scenarios.BusinessLogic(login="ksavinov", url="http://orange.polymatica.ru:480", jupiter=True)
        sc.get_cube(cube_name="mee ИП в отношении ЮЛ (+Регион ОСП)")
        sc.move_dimension(dim_name="Федеральный округ ОСП", position="left", level=0)
        # выделить факт "Сумма долга"
        measure_id = sc.get_measure_id(measure_name="Сумма долга")
        sc.execute_olap_command(command_name="fact", state="set_selection", fact=measure_id,
                                is_seleceted=True)
        # 15. Создать график с типом Линии (тип по умолчанию)
        sc.execute_manager_command(command_name="user_iface",
                                   state="create_module",
                                   module_id=sc.multisphere_module_id,
                                   module_type=600,
                                   layer_id=sc.active_layer_id,
                                   after_module_id=sc.multisphere_module_id)
        # 16. Создать копию OLAP-модуля
        sc.clone_current_olap_module()
        # выставить ширину колонок
        sc.set_width_columns(left_dims=[100], measures=[154, 210])
        sc.logout()

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_dim_filers(self):
        sc = business_scenarios.BusinessLogic(login="ksavinov", url="http://orange.polymatica.ru:480", jupiter=True)
        sc.get_cube(cube_name="mee ИП в отношении ЮЛ (+Регион ОСП)")
        sc.move_dimension(dim_name="Дата возбуждения дата", position="left", level=0)

        # отметить фильтры и проверить корректность количества отмеченных фильтров
        sc.put_dim_filter(dim_name="Дата возбуждения дата", filter_name=["2001-02-20", "2008-10-07"])
        dim_id = sc.get_dim_id(dim_name="Дата возбуждения дата")
        result = sc.h.get_filter_rows(dim_id)
        filters_values = sc.h.parse_result(result=result, key="marks")  # получить список on/off [0,0,...,0]
        counter = collections.Counter(filters_values)
        assert counter[1] == 2

        sc.put_dim_filter(dim_name="Дата возбуждения", filter_name="2006-03-07 00:00:00")
        dim_id = sc.get_dim_id(dim_name="Дата возбуждения")
        result = sc.h.get_filter_rows(dim_id)
        filters_values = sc.h.parse_result(result=result, key="marks")  # получить список on/off [0,0,...,0]
        counter = collections.Counter(filters_values)
        assert counter[1] == 1

        sc.put_dim_filter(dim_name="Дата возбуждения год", start_date=2009, end_date=2016)
        dim_id = sc.get_dim_id(dim_name="Дата возбуждения год")
        result = sc.h.get_filter_rows(dim_id)
        filters_values = sc.h.parse_result(result=result, key="marks")  # получить список on/off [0,0,...,0]
        counter = collections.Counter(filters_values)
        marked_filters = 2016 - 2009
        assert counter[1] == marked_filters + 1

        res = sc.put_dim_filter(dim_name="Дата возбуждения день недели", start_date="Воскресенье", end_date="Понедельник")
        assert "Start week day can not be more than the end week day" in res

        sc.put_dim_filter(dim_name="Дата возбуждения день недели", start_date="Пятница", end_date="Воскресенье")
        dim_id = sc.get_dim_id(dim_name="Дата возбуждения день недели")
        result = sc.h.get_filter_rows(dim_id)
        filters_values = sc.h.parse_result(result=result, key="marks")  # получить список on/off [0,0,...,0]
        counter = collections.Counter(filters_values)
        assert counter[1] == 3

        sc.put_dim_filter(dim_name="Дата возбуждения месяц", start_date="Январь", end_date="Май")
        dim_id = sc.get_dim_id(dim_name="Дата возбуждения месяц")
        result = sc.h.get_filter_rows(dim_id)
        filters_values = sc.h.parse_result(result=result, key="marks")  # получить список on/off [0,0,...,0]
        counter = collections.Counter(filters_values)
        assert counter[1] == 5

        sc.put_dim_filter(dim_name="Дата возбуждения число", start_date=5, end_date=30)
        dim_id = sc.get_dim_id(dim_name="Дата возбуждения число")
        result = sc.h.get_filter_rows(dim_id)
        filters_values = sc.h.parse_result(result=result, key="marks")  # получить список on/off [0,0,...,0]
        counter = collections.Counter(filters_values)
        marked_filters = 30 - 5
        assert counter[1] == marked_filters + 1

        sc.put_dim_filter(dim_name="Дата исполнительного документа", start_date="2001-04-09 00:00:00",
                          end_date="2001-05-23 00:00:00")
        dim_id = sc.get_dim_id(dim_name="Дата исполнительного документа")
        result = sc.h.get_filter_rows(dim_id)
        filters_values = sc.h.parse_result(result=result, key="marks")  # получить список on/off [0,0,...,0]
        counter = collections.Counter(filters_values)
        assert counter[1] == 20

        sc.put_dim_filter(dim_name="Дата исполнительного документа дата", start_date="2001-02-18",
                          end_date="2001-03-01")
        dim_id = sc.get_dim_id(dim_name="Дата исполнительного документа дата")
        result = sc.h.get_filter_rows(dim_id)
        filters_values = sc.h.parse_result(result=result, key="marks")  # получить список on/off [0,0,...,0]
        counter = collections.Counter(filters_values)
        assert counter[1] == 10

        sc.logout()

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_create_sphere_csv_scheduled_upd(self):
        sc = business_scenarios.BusinessLogic(login="ksavinon", password="ksavinon",
                                              url="https://r5611u16.polymatica.ru", jupiter=True)

        # предусловия
        my_cube_name = "savinov_test01"
        update_params = {"type": "по расписанию",
                         "schedule": {"type": "Ежедневно", "time": "18:30", "time_zone": "UTC+3:00"}}

        # Создать мультисферу
        sc.create_sphere(cube_name=my_cube_name, filepath="MyCube_Countries_import.csv",
                         source_name="источник", file_type="csv", encoding="UTF-8", separator=";",
                         update_params=update_params, user_interval="с предыдущего дня", delayed=False)

        # Дождаться загрузки мультисферы
        sc.wait_cube_loading(cube_name=my_cube_name)

        # Удалить мультисферу!
        cube_id = sc.get_cube_without_creating_module(cube_name=my_cube_name)
        sc.execute_manager_command(command_name="resource", state="delete", resource_id=cube_id)

        # проверить, что куб удален
        result = sc.execute_manager_command(command_name="user_cube", state="list_request")
        cubes_list = sc.h.parse_result(result=result, key="cubes")
        cubes_list = [cube["name"] for cube in cubes_list]
        assert my_cube_name not in cubes_list

        sc.logout()

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_create_sphere_xls_manual_upd(self):
        sc = business_scenarios.BusinessLogic(login="ksavinov", url="http://orange.polymatica.ru:480", jupiter=True)

        # предусловия
        my_cube_name = "savinov_test01"
        update_params = {"type": "ручное"}

        # Создать мультисферу
        sc.create_sphere(cube_name=my_cube_name, filepath="savinov_sphere_0_20-05-28_12_39_29.xlsx",
                         source_name="источник", file_type="excel", update_params=update_params,
                         user_interval="с текущего дня")

        # Дождаться загрузки мультисферы
        sc.wait_cube_loading(cube_name=my_cube_name)

        # Удалить мультисферу!
        cube_id = sc.get_cube_without_creating_module(cube_name=my_cube_name)
        sc.execute_manager_command(command_name="resource", state="delete", resource_id=cube_id)

        # проверить, что куб удален
        result = sc.execute_manager_command(command_name="user_cube", state="list_request")
        cubes_list = sc.h.parse_result(result=result, key="cubes")
        cubes_list = [cube["name"] for cube in cubes_list]
        assert my_cube_name not in cubes_list

        sc.logout()

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_inc_upd_sphere(self):
        sc = business_scenarios.BusinessLogic(login="ksavinon", password="ksavinon",
                                              url="https://r5611u16.polymatica.ru", jupiter=True)

        # предусловия
        cube_name = "1112POSTGRES"

        update_params = {"type": "инкрементальное",
                         "schedule": {"type": "Ежедневно", "time": "18:30", "time_zone": "UTC+3:00"}}

        # обновить куб
        sc.update_cube(cube_name=cube_name, update_params=update_params, increment_dim="checkdate")

        # дождаться загрузки куба
        sc.wait_cube_loading(cube_name)

        # проверить, что куб обновлен
        result = sc.execute_manager_command(command_name="user_cube", state="list_request")
        cubes = sc.h.parse_result(result, "cubes")
        for cube in cubes:
            if cube["name"] == cube_name:
                assert cube["is_updated"] is True

        sc.logout()

    # @pytest.mark.skip(reason="no way of currently testing this")
    def test_interval_upd_sphere(self):
        sc = business_scenarios.BusinessLogic(login="ksavinon", password="ksavinon",
                                              url="https://r5611u16.polymatica.ru", jupiter=True)

        # предусловия
        cube_name = "1112POSTGRES"
        update_params = {"type": "интервальное",
                         "schedule": {"type": "Ежедневно", "time": "18:30", "time_zone": "UTC+3:00"}}

        # обновить куб
        sc.update_cube(cube_name=cube_name, update_params=update_params)

        # Дождаться загрузки мультисферы
        sc.wait_cube_loading(cube_name=cube_name)

        # проерить, что куб обновлен
        result = sc.execute_manager_command(command_name="user_cube", state="list_request")
        cubes = sc.h.parse_result(result, "cubes")
        for cube in cubes:
            if cube["name"] == cube_name:
                assert cube["is_updated"] is True

        sc.logout()
