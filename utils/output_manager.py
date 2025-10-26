import os
import re
from datetime import datetime
from typing import List

class OutputManager:
    """
    Output manager responsible for saving query results to files
    """
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """Ensure output directory exists"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def _extract_city_from_prompt(self, prompt: str) -> str:
        """Extract city name from user request"""
        # Chinese cities (including common aliases)
        chinese_cities = {
            'Beijing': ['北京', 'Beijing', '帝都'],
            'Shanghai': ['上海', 'Shanghai', '魔都'],
            'Guangzhou': ['广州', 'Guangzhou', '羊城'],
            'Shenzhen': ['深圳', 'Shenzhen', '鹏城'],
            'Hangzhou': ['杭州', 'Hangzhou', '西湖'],
            'Nanjing': ['南京', 'Nanjing', '金陵'],
            'Suzhou': ['苏州', 'Suzhou', '姑苏'],
            'Chengdu': ['成都', 'Chengdu', '蓉城'],
            'Chongqing': ['重庆', 'Chongqing', '山城'],
            'Xian': ['西安', "Xi'an", '长安'],
            'Wuhan': ['武汉', 'Wuhan', '江城'],
            'Tianjin': ['天津', 'Tianjin'],
            'Qingdao': ['青岛', 'Qingdao'],
            'Dalian': ['大连', 'Dalian'],
            'Xiamen': ['厦门', 'Xiamen', '鹭岛'],
            'Changsha': ['长沙', 'Changsha', '星城'],
            'Zhengzhou': ['郑州', 'Zhengzhou'],
            'Jinan': ['济南', 'Jinan', '泉城'],
            'Harbin': ['哈尔滨', 'Harbin', '冰城'],
            'Shenyang': ['沈阳', 'Shenyang'],
            'Changchun': ['长春', 'Changchun'],
            'Kunming': ['昆明', 'Kunming', '春城'],
            'Guiyang': ['贵阳', 'Guiyang'],
            'Nanning': ['南宁', 'Nanning'],
            'Haikou': ['海口', 'Haikou'],
            'Sanya': ['三亚', 'Sanya'],
            'Lhasa': ['拉萨', 'Lhasa'],
            'Urumqi': ['乌鲁木齐', 'Urumqi'],
            'Yinchuan': ['银川', 'Yinchuan'],
            'Xining': ['西宁', 'Xining'],
            'Lanzhou': ['兰州', 'Lanzhou'],
            'Hohhot': ['呼和浩特', 'Hohhot'],
            'Shijiazhuang': ['石家庄', 'Shijiazhuang'],
            'Taiyuan': ['太原', 'Taiyuan'],
            'Hefei': ['合肥', 'Hefei'],
            'Nanchang': ['南昌', 'Nanchang'],
            'Fuzhou': ['福州', 'Fuzhou'],
            'Wuxi': ['无锡', 'Wuxi'],
            'Changzhou': ['常州', 'Changzhou'],
            'Ningbo': ['宁波', 'Ningbo'],
            'Wenzhou': ['温州', 'Wenzhou'],
            'Jiaxing': ['嘉兴', 'Jiaxing'],
            'Jinhua': ['金华', 'Jinhua'],
            'Shaoxing': ['绍兴', 'Shaoxing'],
            'Taizhou': ['台州', 'Taizhou'],
            'Huzhou': ['湖州', 'Huzhou'],
            'Lishui': ['丽水', 'Lishui'],
            'Quzhou': ['衢州', 'Quzhou'],
            'Zhoushan': ['舟山', 'Zhoushan']
        }
        
        # International cities (including common aliases)
        international_cities = {
            'Taipei': ['台北', 'Taipei'],
            'Hong Kong': ['香港', 'Hong Kong', 'HK'],
            'Macau': ['澳门', 'Macau', 'Macao'],
            'Singapore': ['新加坡', 'Singapore', '狮城'],
            'Kuala Lumpur': ['吉隆坡', 'Kuala Lumpur', 'KL'],
            'Bangkok': ['曼谷', 'Bangkok'],
            'Tokyo': ['东京', 'Tokyo'],
            'Seoul': ['首尔', 'Seoul', '汉城'],
            'New York': ['纽约', 'New York', 'NYC'],
            'London': ['伦敦', 'London'],
            'Paris': ['巴黎', 'Paris'],
            'Sydney': ['悉尼', 'Sydney'],
            'Toronto': ['多伦多', 'Toronto'],
            'Vancouver': ['温哥华', 'Vancouver'],
            'Los Angeles': ['洛杉矶', 'Los Angeles', 'LA'],
            'San Francisco': ['旧金山', 'San Francisco', 'SF'],
            'Chicago': ['芝加哥', 'Chicago'],
            'Washington': ['华盛顿', 'Washington', 'DC'],
            'Boston': ['波士顿', 'Boston'],
            'Seattle': ['西雅图', 'Seattle'],
            'Miami': ['迈阿密', 'Miami'],
            'Las Vegas': ['拉斯维加斯', 'Las Vegas', '赌城'],
            'Berlin': ['柏林', 'Berlin'],
            'Munich': ['慕尼黑', 'Munich'],
            'Amsterdam': ['阿姆斯特丹', 'Amsterdam'],
            'Brussels': ['布鲁塞尔', 'Brussels'],
            'Rome': ['罗马', 'Rome'],
            'Milan': ['米兰', 'Milan'],
            'Barcelona': ['巴塞罗那', 'Barcelona'],
            'Madrid': ['马德里', 'Madrid'],
            'Moscow': ['莫斯科', 'Moscow'],
            'Saint Petersburg': ['圣彼得堡', 'Saint Petersburg'],
            'Dubai': ['迪拜', 'Dubai'],
            'Cairo': ['开罗', 'Cairo'],
            'Melbourne': ['墨尔本', 'Melbourne'],
            'Brisbane': ['布里斯班', 'Brisbane'],
            'Valencia': ['瓦伦西亚', 'Valencia'],
            'Granada': ['格拉纳达', 'Granada'],
            'Seville': ['塞维利亚', 'Sevilla', 'Seville'],
            'Bilbao': ['毕尔巴鄂', 'Bilbao'],
            'Zaragoza': ['萨拉戈萨', 'Zaragoza'],
            'Malaga': ['马拉加', 'Malaga'],
            'Murcia': ['穆尔西亚', 'Murcia'],
            'Palma': ['帕尔马', 'Palma'],
            'Las Palmas': ['拉斯帕尔马斯', 'Las Palmas'],
            'Cordoba': ['科尔多瓦', 'Cordoba'],
            'Alicante': ['阿利坎特', 'Alicante'],
            'Vigo': ['维戈', 'Vigo'],
            'Gijon': ['希洪', 'Gijon'],
            'Oviedo': ['奥维耶多', 'Oviedo'],
            'Santiago de Compostela': ['圣地亚哥德孔波斯特拉', 'Santiago de Compostela'],
            'Toledo': ['托莱多', 'Toledo'],
            'Caceres': ['卡塞雷斯', 'Caceres'],
            'Badajoz': ['巴达霍斯', 'Badajoz'],
            'Avila': ['阿维拉', 'Avila'],
            'Segovia': ['塞哥维亚', 'Segovia'],
            'Salamanca': ['萨拉曼卡', 'Salamanca'],
            'Burgos': ['布尔戈斯', 'Burgos'],
            'Leon': ['莱昂', 'Leon'],
            'Palencia': ['帕伦西亚', 'Palencia'],
            'Valladolid': ['瓦拉多利德', 'Valladolid'],
            'Zamora': ['萨莫拉', 'Zamora'],
            'Logrono': ['洛格罗尼奥', 'Logrono'],
            'Pamplona': ['潘普洛纳', 'Pamplona'],
            'San Sebastian': ['圣塞巴斯蒂安', 'San Sebastian'],
            'Vitoria': ['维多利亚', 'Vitoria'],
            'Huesca': ['韦斯卡', 'Huesca'],
            'Teruel': ['特鲁埃尔', 'Teruel'],
            'Castellon': ['卡斯特利翁', 'Castellon'],
            'Jaen': ['哈恩', 'Jaen'],
            'Almeria': ['阿尔梅里亚', 'Almeria'],
            'Cadiz': ['加的斯', 'Cadiz'],
            'Huelva': ['韦尔瓦', 'Huelva'],
            'Jerez': ['赫雷斯', 'Jerez'],
            'Algeciras': ['阿尔赫西拉斯', 'Algeciras'],
            'Marbella': ['马贝拉', 'Marbella'],
            'Estepona': ['埃斯特波纳', 'Estepona'],
            'Fuengirola': ['富恩希罗拉', 'Fuengirola'],
            'Torremolinos': ['托雷莫利诺斯', 'Torremolinos'],
            'Benalmadena': ['贝纳尔马德纳', 'Benalmadena'],
            'Ronda': ['龙达', 'Ronda']
        }
        
        # Merge all cities
        all_cities = {**chinese_cities, **international_cities}
        
        # Preprocess text, remove common country prefixes
        processed_prompt = prompt.lower()
        country_prefixes = ['西班牙', '意大利', '法国', '德国', '英国', '美国', '日本', '韩国', '泰国', '新加坡', '马来西亚', '澳大利亚', '加拿大', '俄罗斯', '荷兰', '比利时', '瑞士', '奥地利', '丹麦', '瑞典', '挪威', '芬兰', 'spain', 'italy', 'france', 'germany', 'uk', 'usa', 'japan', 'korea', 'thailand', 'singapore', 'malaysia', 'australia', 'canada', 'russia', 'netherlands', 'belgium', 'switzerland', 'austria', 'denmark', 'sweden', 'norway', 'finland']
        
        # Sort cities by name length, prioritize matching longer names (avoid partial matching issues)
        for city_name, aliases in sorted(all_cities.items(), key=lambda x: max(len(alias) for alias in x[1]), reverse=True):
            for alias in aliases:
                # Direct matching
                if alias.lower() in processed_prompt:
                    return city_name
                
                # Try matching with country prefix
                for prefix in country_prefixes:
                    if f"{prefix}{alias}" in prompt or f"{prefix} {alias}" in prompt:
                        return city_name
        
        return "Query City"
    
    def _generate_filename(self, city: str) -> str:
        """Generate filename: datetime_cityname"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Clean city name, remove possible special characters
        clean_city = re.sub(r'[<>:"/\\|?*]', '', city)
        return f"{timestamp}_{clean_city}.txt"
    
    def save_travel_report(self, user_prompt: str, final_answer: str, 
                          prompt_history: List[str]) -> str:
        """
        Save travel query report
        
        Args:
            user_prompt: User's original request
            final_answer: Final answer
            prompt_history: Complete conversation history
            
        Returns:
            Saved file path
        """
        city = self._extract_city_from_all_content(user_prompt, final_answer, prompt_history)
        filename = self._generate_filename(city)
        filepath = os.path.join(self.output_dir, filename)
        
        # Prepare output content
        content = self._format_travel_report(user_prompt, final_answer, 
                                           prompt_history, city)
        
        # Write to file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return filepath
        except Exception as e:
            raise Exception(f"Error saving file: {e}")
    
    def _extract_city_from_all_content(self, user_prompt: str, final_answer: str, 
                                     prompt_history: List[str]) -> str:
        """
        Extract city name from user request, final answer and conversation history
        Prioritize maintaining the original city name format from user request
        
        Args:
            user_prompt: User's original request
            final_answer: Final answer
            prompt_history: Complete conversation history
            
        Returns:
            Extracted city name
        """
        # First try to extract from user request, maintaining original format
        original_city = self._extract_original_city_from_prompt(user_prompt)
        if original_city != "Query City":
            return original_city
        
        # If original format not found, use standardized extraction
        city = self._extract_city_from_prompt(user_prompt)
        if city != "Query City":
            return city
        
        # If not found in user request, try to extract city info from tool calls
        for entry in prompt_history:
            if "get_weather" in entry or "get_attraction" in entry or "calculate_budget" in entry:
                # Extract city parameter from tool calls
                city_match = re.search(r'city="([^"]*)"', entry)
                if city_match:
                    extracted_city = city_match.group(1)
                    # Verify if extracted city is in our city list
                    verified_city = self._extract_city_from_prompt(extracted_city)
                    if verified_city != "Query City":
                        return verified_city
                    # If not in list, use extracted city name directly
                    return extracted_city
        
        # If not found in final answer either, try to extract from final answer
        city = self._extract_city_from_prompt(final_answer)
        if city != "Query City":
            return city
        
        # If not found in conversation history either, try to extract from conversation history
        for entry in prompt_history:
            city = self._extract_city_from_prompt(entry)
            if city != "Query City":
                return city
        
        return "Travel Query"
    
    def _extract_original_city_from_prompt(self, prompt: str) -> str:
        """
        Extract original city name format from user request (including country prefix)
        
        Args:
            prompt: User request text
            
        Returns:
            Extracted original city name
        """
        # Common city name patterns (including country prefix)
        city_patterns = [
            # Spanish cities - exact matching
            r'西班牙(格拉纳达|马德里|巴塞罗那|瓦伦西亚|塞维利亚|龙达|毕尔巴鄂|萨拉戈萨|马拉加|穆尔西亚|帕尔马|科尔多瓦|阿利坎特|托莱多|萨拉曼卡|布尔戈斯|莱昂|瓦拉多利德|洛格罗尼奥|潘普洛纳|圣塞巴斯蒂安|维多利亚)',
            r'Spain\s+(Granada|Madrid|Barcelona|Valencia|Seville|Sevilla|Ronda|Bilbao|Zaragoza|Malaga|Murcia|Palma|Cordoba|Alicante|Toledo|Salamanca|Burgos|Leon|Valladolid|Logrono|Pamplona)',
            # Other country cities
            r'意大利(罗马|米兰|佛罗伦萨|威尼斯|那不勒斯|都灵|博洛尼亚|巴勒莫|热那亚|卡塔尼亚)',
            r'Italy\s+(Rome|Milan|Florence|Venice|Naples|Turin|Bologna|Palermo|Genoa|Catania)',
            r'法国(巴黎|马赛|里昂|图卢兹|尼斯|南特|斯特拉斯堡|蒙彼利埃|波尔多|里尔)',
            r'France\s+(Paris|Marseille|Lyon|Toulouse|Nice|Nantes|Strasbourg|Montpellier|Bordeaux|Lille)',
            r'德国(柏林|慕尼黑|汉堡|科隆|法兰克福|斯图加特|杜塞尔多夫|多特蒙德|埃森|莱比锡)',
            r'Germany\s+(Berlin|Munich|Hamburg|Cologne|Frankfurt|Stuttgart|Dusseldorf|Dortmund|Essen|Leipzig)',
            r'英国(伦敦|曼彻斯特|伯明翰|利兹|格拉斯哥|谢菲尔德|布拉德福德|爱丁堡|利物浦|布里斯托)',
            r'UK\s+(London|Manchester|Birmingham|Leeds|Glasgow|Sheffield|Bradford|Edinburgh|Liverpool|Bristol)',
            r'美国(纽约|洛杉矶|芝加哥|休斯顿|费城|凤凰城|圣安东尼奥|圣地亚哥|达拉斯|圣何塞)',
            r'USA\s+(New York|Los Angeles|Chicago|Houston|Philadelphia|Phoenix|San Antonio|San Diego|Dallas|San Jose)',
        ]
        
        for pattern in city_patterns:
            match = re.search(pattern, prompt)
            if match:
                city_name = match.group(1).strip()
                if city_name:
                    return city_name
        
        return "Query City"
    
    def _format_travel_report(self, user_prompt: str, final_answer: str, 
                            prompt_history: List[str], city: str) -> str:
        """Format travel report content"""
        lines = []
        
        # Report header
        lines.append("=" * 80)
        lines.append("🌍 Smart Travel Assistant - Query Results Report")
        lines.append("=" * 80)
        lines.append(f"📅 Query Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"🏙️  Query City: {city}")
        lines.append(f"🔍 Query ID: {datetime.now().strftime('%Y%m%d%H%M%S')}")
        lines.append("")
        
        # User request
        lines.append("📝 User Request:")
        lines.append("-" * 50)
        lines.append(user_prompt)
        lines.append("")
        
        # Final answer
        lines.append("✅ Final Answer:")
        lines.append("-" * 50)
        lines.append(final_answer)
        lines.append("")
        
        # Detailed execution process
        lines.append("🔄 Detailed Execution Process:")
        lines.append("-" * 50)
        for i, entry in enumerate(prompt_history, 1):
            lines.append(f"[Step {i}] {entry}")
            lines.append("")
        
        # Report footer
        lines.append("=" * 80)
        lines.append("📊 Report Statistics:")
        lines.append(f"   • Total execution steps: {len(prompt_history)}")
        lines.append(f"   • Report generation time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 80)
        lines.append("🎯 Smart Travel Assistant - Making Travel Smarter")
        lines.append("=" * 80)
        
        return '\n'.join(lines)
    
    def list_saved_reports(self) -> List[str]:
        """List all saved report files"""
        if not os.path.exists(self.output_dir):
            return []
        
        files = []
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.output_dir, filename)
                files.append(filepath)
        
        return sorted(files, reverse=True)  # Sort by time in descending order