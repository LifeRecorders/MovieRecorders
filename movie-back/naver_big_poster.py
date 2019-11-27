## movie 이름으로 검색하고,
## code=190106 를 찾아서 
## https://movie.naver.com/movie/bi/mi/basic.nhn?code=190106
### 장고 모델의 link에서 다음과 같이 코드를 받을 수 있음

## https://movie.naver.com/movie/bi/mi/basic.nhn?code=99227
## https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=190106
## undefined
from pprint import pprint
from time import sleep
import urllib3
import re


# crawling용
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from decouple import config

# django db 저장용
import json
import os
import django


# Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movieback.settings")
django.setup()
from movies.models import *

errorlist = []

movies = Movie.objects.exclude(naver_link__exact='')
print(movies)

for movie in movies:
    # naver_link가 있다면,
    sleep(0.005)
    movieCode = movie.naver_link[51:]
    base_url = f'https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode={movieCode}'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    if soup.select_one('#targetImage') == None:
        continue
    image = soup.select_one('#targetImage')['src']  
    movie.naver_big_poster_url = image
    movie.save()

'''
1# error
['39359', '41170', '100595', '99227', '190106', '42157', '118968', '38766', '85627', '62773', '89866', '97976', '39911', '41361', '39658', '36728', '40163', '39512', '41363', '160920', '190163', '39715', '184724', '52954', '187924', '191092', '40887', '40322', '39405', '43151', '38318', '41399', '39846', '41438', '42810', '38855', '104621', '182852', '112742', '41376', '169263', '40222', '42845', '39818', '39601', '101180', '38824', '44006', '43158', '43502', '97660', '136872', '43510', '172486', '39626', '182205', '39906', '40098', '43844', '180632', '127868', '43610', '39624', '183551', '52786', '40134', '85533', '37883', '39652', '120969', '146548', '179302', '43678', '188162', '58023', '189520', '60510', '57412', '60307', '144095', '58255', '57950', '181959', '164160', '52307', '46314', '167632', '57335', '45749', '42506', '87364', '43396', '57987', '57486', '57598', '92084', '57805', '189014', '61104', '58273', '57687', '167108', '46330', '136662', '62960', '62626', '62742', '57874', '57961', '57729', '100364', '189303', '160312', '45033', '91796', '189969', '41586', '45118', '58085', '96951', '85544', '159853', '61658', '45529', '56038', '147761', '101932', '150942', '61535', '60484', '61025', '102347', '172584', '162536', '188656', '58288', '14584', '101975', '94125', '55872', '57675',
'134136', '44354', '61184', '99647', '57794', '77117', '64126', '42117', '44008', '164989', '180002', '144903', '187347', '148854', '43679', '57758', '43838', '66195', '168902', '188107', '66647', '65535', '68034', '67635', '66189', '164168', '64991', '65642', '57095', '123630', '64995', '40133', '65021', '159865', '160083', '61506', '65092', '183826', '189812', '66625', '180428', '65735', '62550', '63017', '63722', '65429', '66793',
'159986', '106572', '67887', '61699', '96847', '65869', '58018', '123568', '65063', '185990', '65532', '175150', '65058', '50620', '65649', '59075', '131859', '61428', '182777', '68333', '63916', '64242', '64245', '187341', '65290', '36778', '45491', '190142', '64093', '53825', '188998', '107755', '184308', '66363', '146932', '62733', '171506', '65540', '64921', '65923', '123221', '184080', '65340', '150081', '65815', '185838', '61706', '169953', '65433', '103774', '122015', '156556', '61101', '167528', '189247', '66158', '113301', '66818', '185969', '62219', '36746', '77143', '125708', '68502', '44898', '109913', '49305', '69266', '81322', '78525', '189468', '186990', '47324', '68944', '68217', '97692', '65669', '105339', '49459', '65842', '64185', '47101', '47339', '154986', '45914', '66569', '143607', '75567', '67883', '148304', '65674', '48598', '69105', '49821', '50097', '45695', '94251', '181104', '173239', '65836', '184182', '183088', '97077', '69917', '189728', '165697', '65213', '183113', '65515', '50679', '168402', '45399', '63824', '69299', '65808', '136462', '66310', '154232', '50704', '69269', '85705', '57666', '66002', '187643', '66729', '89117', '46137', '45292', '133059', '92083', '171827', '168190', '168565', '164115', '50185', '69467', '67533', '65610', '45280', '68880', '84915', '65197', '45941', '49525', '85149', '171907', '129847', '183826', '66464', '181692', '148645', '50621', '52543', '49852', '51856', '53159', '50903', '49483', '52063', '50672', '45521', '91671', '68052', '54847', '67900', '182217', '181462', '52504', '69951', '189793', '52413', '83013', '45938', '51452', '68038', '53758', '49228', '47494', '53000', '52449', '47425', '54704', '45979', '149287', '155406', '52528', '188889', '70123', '184516', '52992', '98693', '70016', '53350', '66724', '164840', '53025', '184828', '141824', '69952', '190541', '45285', '55060', '178258', '51407', '67061', '57865', '163645', '84251', '108785', '54290', '52074', '64129', '190818', '71588', '70251', '49529', '52245', '153067', '52792', '71901', '148929', '68086', '52375', '52424', '189388', '54973', '52516', '184519', '83095', '74124', '109494', '163031', '178829', '189091', '189048', '72718', '189304', '70637', '155242', '180142', '70118', '47381', '109168', '158852', '97642', '70395', '76347', '74904', '126386', '73411', '79159', '163711', '52525', '79140', '76454', '76560', '172391', '172373', '123407', '171383', '81784', '185952', '47528', '74315', '178751', '85094', '48246', '78073', '79425', '147898', '69994', '163933', '118966', '41585', '190198', '84631', '82434', '72562', '74799', '82435', '80629', '145939', '112846', '63538', '181541', '124514', '104364', '82142', '83410', '118981', '190377', '83084', '116123', '83084', '51877', '184102', '82440', '176912', '75413', '76051', '187564', '180169', '82436', '138588', '80193', '152697', '177712', '82219', '84065', '172836', '114279', '143294', '82387', '81316', '190848', '154598', '189205', '51786', '76460', '85660', '138619', '89752', '83017', '80866', '74567', '81106', '70995', '86347', '86129', '84843', '78851', '76048', '73508', '186026', '53372', '182698', '92412', '82227', '83893', '165993', '72054', '95769', '85702', '91391', '72560', '94506', '76955', '93089', '86888', '158647', '93090', '79826', '72076', '184730', '85855', '49728', '83741', '137350', '74156', '164179', '94190', '182756', '104426', '92471', '76956', '124476', '87246', '86319', '88258', '88453', '182000', '92131', '140461', '85659', '178923', '83214', '86023', '91603', '161944', '86197', '76691', '91452', '168727', '157974', '92599', '70994', '88473', '92827', '95501', '135725', '87067', '78720', '92576', '77566', '83893', '152267', '84321', '188907', '88253', '173124', '96978', '96377', '145190', '90885', '152632', '96969', '68073', '91045', '185276', '72270', '177020', '95503', '106335', '112287', '40112', '87216', '102241', '184492', '183489', '80998', '96325', '100100', '99794', '167084', '171930', '174484', '143733', '169810', '171336', '113344', '105389', '62328', '77598', '173468', '84216', '93158', '104331', '98404', '97158', '172780', '160864', '114212', '113873', '75415', '96372', '184919', '98970', '148632', '92176', '98997', '185463', '93017', '130739', '97696', '98467', '186041', '187935', '189737', '189976', '163806', '103762', '110953', '136035', '165461', '96997', '94136', '189651', '182372', '95873', '93757', '92081', '112031', '81315', '188743', '85857', '94170', '132787', '167615', '100950', '103719', '101700', '103343', '149629', '100930', '161039', '187107', '92075', '74566', '137865', '149909', '125822', '113170', '106065', '99752', '43199', '173124', '123420', '76020', '119962', '114261', '98485', '114146', '118921', '109753', '115503', '118370', '137908', '122581', '45715', '118931', '133253', '116532', '189101', '174616', '167696', '176524', '94829', '102817', '95557', '125826', '67769', '176888', '118974', '181938', '121047', '134641', '113342', '183850', '125426', '101972', '177221', '128235', '103683', '118377', '154814', '179362', '113312', '100828', '102953', '153196', '129782', '161263', '186341', '171020', '109971', '138067', '175324', '126156', '109200', '101953', '173453', '94112', '101939', '100643', '118409', '183286', '39640', '112079', '190907', '109955', '118173', '107370', '113377', '121132', '149545', '130013', '97816', '102875', '118323', '190026', '98149', '134136', '136832', '118968', '187825', '132991', '95541', '117802', '130787', '113351', '122469', '137973', '129406', '130957', '118376', '154269', '130765', '153552', '129050', '142010', '144330', '115296', '189771', '140015', '174616', '134685', '181816', '129408', '140139', '188840', '118954', '181554', '187439', '181711', '130978', '124201', '163846', '129051', '186258', '120793', '124240', '90591', '136007', '125405', '180425', '51055', '185696', '127375', '154599', '164172', '129333', '186245', '121094', '174756', '158751', '175104', '38444', '111990', '99701', '124013', '135807', '178566', '100643', '81967', '125466', '162352', '128258', '115520', '187348', '120157', '114225', '140711', '132610', '143253', '99748',
'121788', '137010', '128392', '187114', '163784', '130786', '149531', '124238', '122596', '177977', '143245', '186056', '137281', '130757', '172819', '145336', '147001', '62285', '177702', '136842', '109910', '157784',
'124212', '148655', '148608', '130850', '128273', '119453', '182408', '136843', '136878', '115504', '139613', '122527', '132998', '181701', '142691', '144310', '146560', '150117', '167599', '119430', '137908', '121051', '75006', '188252', '125802', '137915', '188746', '130720', '188674', '53152', '144780', '127394', '74866', '114282', '120791', '188607', '183414', '139700', '153296', '179127', '134895', '146311', '137884', '189140', '113344', '127378', '146548', '97629', '131576', '149049', '144968', '115620', '167569', '122195', '141824', '140730', '185860', '127361', '142822', '180374', '125414', '130966', '182578', '94767', '130987', '144918', '190505', '145318', '93929', '147834', '152169', '190067', '133447', '118953', '143456', '143495', '133129', '140693', '136835', '125468', '137952', '118966', '140731', '144280', '156259', '127346', '153964', '99715', '127374', '176225', '127398', '154112', '144988', '156417', '160964', '156091', '163027', '175372', '149221', '129094', '159521', '152309', '82473', '176398', '163834', '182896', '183877', '164342', '155256', '187351', '188377', '171415', '148994', '160464', '182408', '149776', '188402', '183666', '123630', '143435', '184439', '154262', '155716', '165029', '158910', '152396', '185755', '187161', '158651', '185969', '173123', '156477', '154458', '159054', '146480', '146506', '165585', '153279', '165025', '189349', '132626', '146407', '152341', '143394', '155680', '144215', '137696', '152170', '165461', '154267', '137970', '162824', '153652', '146469', '125401', '167035', '70627', '167560', '137945', '151674', '159516', '165514', '143402', '137890', '152625', '125439', '156200', '188980', '140696', '121052', '88227', '190902', '149747', '164968', '162113', '169561', '157178', '150637', '154353', '183408', '129095', '172836', '143250', '152268', '183426', '142317', '175318', '158576', '162932', '160749', '142210', '169850', '155715', '179340', '166008', '181411', '134898', '184229', '189748', '134963', '155411', '100205', '181029', '154272', '125418', '168508', '152385', '160399', '113221', '159037', '150688', '125488', '168501', '163844', '169349', '150198', '165722', '165030', '188909', '160491',
'142272', '172006', '144381', '163834', '152656', '151254', '171727', '149504', '152249', '163842', '172009', '171664', '165791', '153651', '149248', '168037', '158647', '106360', '85579', '158180', '159805', '182021',
'66725', '146489', '165748', '158112', '154598', '188088', '151744', '159862', '190278', '151752', '164719', '118955', '184516', '141206', '158626', '158601', '158631', '158610', '153620', '165026', '171752', '154449',
'150658', '171440', '125494', '158885', '85578', '187453', '165561', '168298', '140235', '151241', '168036', '171403', '172454', '158555', '136898', '154667', '189388', '163664', '189368', '157974', '162249', '162874',
'173004', '171401', '173653', '172034', '157243', '94131', '154251', '173466', '164684', '174617', '169347', '170139', '172151', '174806', '179841', '171441', '147388', '167100', '144693', '164183', '189276', '189361',
'136900', '174804', '162854', '149236', '174878', '68291', '172420', '175617', '169240', '164121', '168017', '168405', '158178', '153675', '152680', '154285', '167787', '170859', '152694', '175365', '159892', '164151',
'172113', '172003', '172344', '143416', '168030', '158178', '160375', '186657', '144330', '174805', '172174', '136990', '175727', '172118', '171499', '152661', '154222', '180901', '169643', '167602', '165479', '148304', '172768', '153687', '177507', '172010', '167697', '164115', '174626', '127335', '140652', '178445', '132996', '156195', '178426', '185166', '170496', '184543', '168049', '152156', '162981', '158620', '164106', '171466', '170824', '78525', '178402', '167481', '177381', '174807', '163533', '168023', '184392', '168047', '168058', '187323', '167105', '155356', '168050', '170879', '172819', '180002', '164155', '160487', '30688', '171750', '179127', '175318', '166610', '154653', '186453', '179126', '176354', '173692', '161868', '144906', '179138', '154255', '189861', '92125', '179683', '174835', '156496', '188710', '169642', '180384', '171452', '171755', '158622', '164192', '172187', '171725', '150688', '157297', '172975', '180379', '164101', '187444', '173019', '166092', '164139', '187339', '156464', '149278', '172137', '180372', '168056', '144318', '189868', '152632', '164172', '174830', '167699', '180220', '125438', '164173', '180687', '181554', '48233', '169078', '151151', '181411', '181409', '33930', '66728', '167629', '109193', '159070', '190784', '181959', '148909', '170953',
'167099', '182206', '177374', '167651', '182360', '171539', '179974', '169263', '149022', '180425', '161984', '172448', '152624', '153580', '148000', '171533', '182348', '163787', '180381', '181912', '183063', '181414', '181419', '140649', '190433', '24830', '173667', '185267', '164200', '159845', '171785', '180399', '188525', '148863', '132623', '147045', '184253', '49336', '182012', '174321', '171470', '159863', '165022', '151550',
'183136', '175366', '184605', '167657', '190001', '181701', '180169', '183132', '185479', '186899', '177371', '137327', '177967', '183870', '181704', '167053', '164125', '137865', '18781', '183820', '97631', '136900', '167633', '179875', '186259', '183666', '179125', '183836', '181698', '183850', '182014', '180209', '183783', '168092', '174834', '179973', '101966', '182001', '161967', '173668', '173123', '185131', '169637', '167599',
'187051', '163788', '178544', '168086', '177510', '180374', '164907', '154672', '181694', '140656', '183666', '167653', '178526', '181700', '182355', '180351', '179158', '185913', '188153', '174903', '179307', '167560', '187366', '175316', '183110', '96951', '159887', '187161', '177909', '187629', '172836', '174797', '164160', '187508', '181692', '159806', '180402', '180024', '182704', '187787', '172764', '175404', '187526', '186349', '180390', '189140', '129282', '182205', '167613', '167635', '185912', '189071', '74407', '184357', '163831', '181114', '167422', '154298', '182387', '167605', '179482', '179159', '189053', '136873']
'''