public class demo {
    /**
    数据类型：
        Java 的数据类型分为两大类：基本类型（primitive type） 和 引用类型（reference type）。
        基本类型（8 种）
        类别	类型名	字面量示例	大小	说明
        整数	byte	127, -10	8 位	范围：-128 ~ 127
        整数	short	32000, -5000	16 位	范围：-32768 ~ 32767
        整数	int	42, -100, 0	32 位	最常用整数类型
        整数	long	100L, -5L	64 位	字面量需加 L 后缀
        浮点	float	3.14f, -0.5f	32 位	字面量需加 f 后缀
        浮点	double	3.14, -0.5, 2e10	64 位	默认浮点类型
        字符	char	'A', '9', '\n'	16 位	使用单引号，Unicode 字符
        布尔	boolean	true, false	—	只有两个值，不能与数字互转
        引用类型
        包括：类（Class）、接口（Interface）、数组（Array）、枚举（Enum）、字符串（String）等。

        类型	字面量示例	说明
        String	"hello", "world"	字符串，使用双引号
        数组	new int[5], {1,2,3}	存储多个同类型元素
        类	new Person()	自定义对象
        空值	null	引用类型的空值（不是基本类型）
    容器：
        容器类型用于**存储多个数据**。Java 中的容器主要分为**数组**和**集合框架（Collection Framework）** 两大类。集合框架提供了丰富的接口和实现类，常用的包括：
        | 接口/类型 | 实现类                     | 是否可变         | 是否有序                                   | 元素是否可重复 | 示例             |
        | --------- | -------------------------- | ---------------- | ------------------------------------------ | -------------- | ---------------- |
        | `List`    | `ArrayList`, `LinkedList`  | 可变             | 有序（按插入顺序）                         | 可重复         | `[1, 2, 2, 3]`   |
        | `Set`     | `HashSet`, `TreeSet`       | 可变             | `HashSet` 无序，`TreeSet` 有序（自然顺序） | 不可重复       | `{1, 2, 3}`      |
        | `Map`     | `HashMap`, `TreeMap`       | 可变             | `HashMap` 无序，`TreeMap` 有序（按键排序） | 键不可重复     | `{"a":1, "b":2}` |
        | `Queue`   | `ArrayDeque`, `LinkedList` | 可变             | 有序（FIFO 或优先级）                      | 可重复         | `[1, 2, 3]`      |
        | 数组      | `int[]`, `String[]` 等     | 可变（长度固定） | 有序                                       | 可重复         | `{1, 2, 3}`      |
        | `String`  | `String`（字符序列）       | 不可变           | 有序                                       | 可重复         | `"hello"`        |
    方法：
        分为静态方法和实例方法。
            静态方法：在类名前调用，不需要创建对象。
            实例方法：在对象前调用，需要先new创建对象。
            方法重载：方法名相同，参数类型不同。
            私有方法：只能在类内部调用，不能在外部调用。
            共有方法：可以在类外部调用。
    */
    public static void main(String[] args) {
        System.out.println("hello world");
    }

    // 方法重载，参数类型不同，方法名相同
    public static void add(int a, int b) {
        System.out.println(a + b);
    }
    public static void add(double a, double b) { //
        System.out.println(a + b);
    }

    

    /*
    lambda 表达式：
        一种匿名函数表示方式，允许将函数作为参数传递给方法，或将代码块作为数据处理，可以理解为可传递的代码块。
        格式：(参数列表) -> {代码块}
        例如：(a, b) -> a + b;
    interface 接口：
        只包含定义，没有方法实现。
        注意：
            lambda只能用于函数式接口
            lambda不能独立存在，必须赋值给函数式接口变量或者作为参数传递。
    */

    /*
    StreamApi: 处理集合数据的函数式编程工具
    为什么需要？
        传统循环处理集合数据，需要for循环和Iterator接口，代码量较大。
        StreamApi 提供了更简洁的语法，可以链式调用多个操作，实现数据的流水线处理。
        例如：
            List<Integer> list = Arrays.asList(1, 2, 3, 4, 5);
            int sum = list.stream().mapToInt(Integer::intValue).sum();
            System.out.println(sum); // 15
            中间操作，终端操作
            可以操作数据库，分组、排序等操作。
        注意：
            1.stream 不会改数据源
            2.一个 stream只能被消费一次，终端操作关闭后，再使用会抛出异常
            3.中间操作是堕性的，如果没有中间操作，不会执行终端操作
    */


    /*
    面向对象编程，类和对象：
        类class：定义了对象的属性和行为
            使用this可以实现链式调用，this不可在静态方法里使用
            静态方法只能直接访问静态成员，不能直接访问实例成员
            实例方法可以访问静态成员和实例成员
        对象object：类的具体实例，包含了类的属性和行为。
        封装Encapsulation: 隐藏内部实现细节，暴露必要接口
        继承Inheritance: 子类可以父类的属性和方法，减少代码重复
            java支持单继承，不支持多继承
            子类会继承父类所有非 private 成员
            子类可以添加新的属性和方法
            子类可以重写父类方法
            super()调用父类构造方法，必须是子类构造方法的第一条语句
            如果父类没有无参构造，子类必须显式调用父类有参构造方法
            super和this一样，不能在静态方法里使用
            方法重写规则：
                1.方法名相同
                2.返回值类型相同
                3. 访问修饰符不能比父类严格，例如父类是protected,子类不能为private
                4.不能重写final方法
                5.方法重写@Override，检查重写是否正确
                方法重写和方法重载不同：
                    方法重写：子类可以重写父类方法，实现不同的行为
                    方法重载：方法名相同，参数类型不同，实现不同的功能
        多态Polymorphism: 不同对象可以调用相同的方法，实现不同的行为
           向上转型：dog和cat都是animal，但是它们的eat方法实现不同,可以都定义为animal类型
           向下转型：animal类型强制转为dog类
                使用父类引用调用方法时，只能调用父类中声明的方法，不能调用子类独有方法
                向下转型应使用instanceof检查，否则可能会报错
                多态只针对方法，不针对属性
    */
    /*
    抽象类和接口：
        抽象类：不能实例化，用于定义公共方法，由子类实现，单继承
        接口：不能实例化，只能被实现，多实现
     + 抽象类：当多个类有共同代码时，使用抽象类。
     + 接口：当需要定义一种行为契约，而且不同类型的类都需要实现时，使用接口。
     + 通常优先接口，以支持更多灵活设计
    */
    /* 抽象类
        子类必须实现所有抽象方法？（问题）
        不能实例化，只能被继承
        可以包含具体方法，供子类直接使用或重写
        可以有构造方法
        可以有任意类型的成员变量
    */ 
    abstract class Animal {
        // 抽象方法
        abstract void eat();
        // 非抽象方法
        public void sleep() {
            System.out.println("sleep");
        }
    }
    /*
    接口
      完全抽象的类型，只包含常量和抽象方法
      类继承只能有一个，接口可以多个
    */
    interface Drawable {
        String TYPE = "drawable";
        //抽象方法： public abstract 可以省略
        void draw();
        // 定义默认方法，可以选择是否重写
        default void draw2() {
            System.out.println("draw2");
        }
    }
    // 实现接口 implements
    class Circle implements Drawable {
        @Override
        public void draw() {
            System.out.println("draw circle");
        }
    }

    /*
    包package:
        用于组织类和接口的机制，避免命名冲突，将功能相关的类分组在一起，形成一个命名空间
        命名规范：全部小写，域名倒序，有意义的名字，不下划线开头
        例如：com.company.project
        
        包描述文件：package-info.java，用于描述包的元数据，例如包的作者、版本、描述等
        包注解：@Deprecated，用于标记包为过时，建议使用其他包代替
        导入：
            import java.io.* 用于导入java.io包下的所有类,不建议
            import java.util.List 精确导入，推荐
    
    额外了解：模块描述文件module-info.java，只能有一个
    */

    /*
    异常：java中的异常
        运行时异常，编译时异常
    注意：
        不要再finally中使用return，否则会覆盖try中的return语句
        finally中抛出的异常会覆盖try中的异常
    
    抛出异常语法：throw new IllegalArgumentException("参数错误");
    throws可以声明多个异常类型，用逗号分隔。
    子类重写父类方法时，抛出的异常不能比父类宽泛。
    自定义异常类：继承Exception检查类异常，RuntimeException非检查类异常
    // try-with-resources方式，代码执行完后自动关闭资源，自动调用close()
      try (InputStream is = new FileInputStream("test.txt")) {
        byte[] bytes = new byte[1024];
        int len = is.read(bytes);
        System.out.println(new String(bytes, 0, len));
        } catch (IOException e) {
            e.printStackTrace();
        }
    */


    
    /*
    反射：
        1.是java的一种运行机制，允许程程序运行时获取任何内部信息（如构造方法，成员方法，字段，注解等）
        2.可以动态创建调用对象的方法，访问对象的属性。
        3.反射使java有了动态性
    为什么需要：
        1.允许在运行时才决定操作哪个类，哪个方法，实现更加灵活的程序设计。
    优点：
        1.动态性
        2.框架基础底层
        3.通用功能实现
    缺点：
        1.性能开销，比常规调用多一步。
        2.破坏封装，可以访问私有成员
        3.安全隐患，可以绕过访问控制，可能引发安全问题
        4.代码可读性差
        5.编译时检查缺失。
    典型场景：
        1.开发框架，spring依赖注入，aop
        2.orm框架，数据库映射到java类
        3.单元测试
        4.动态代理
        5.配置文件解析
        6.开发工具
    */
    // 获取Class对象
    // 1.通过类名获取
    Class<Integer> clazz = int.class; // 基本数据类型也可以
    // 2.通过对象获取
    Student s = new Student();
    Class<Student> clazz2 = s.getClass(); // 运行时类型
    // 3.最主流，通过 Class.forName() 方法获取
    try {
        Class<?> clazz3 = Class.forName("com.company.project.Student");
    } catch (ClassNotFoundException e) {
        e.printStackTrace();
    }
    /*
    获取构造方法：
    getConstructors()
    getDeclaredConstructors()
    获取成员方法：
    getMethods()
    getDeclaredMethods()
    获取字段：
    getFields()
    getDeclaredFields()
    */

    //==================================================

    /*
    泛型Generics：
    1.允许在定义类，接口和方法使用类型参数
    2.本质是参数化类型，即类型本事可以作为参数传递
    为什么需要：
    1.类型不安全
    2.需要强制类型转换
    泛型名词约定：
    T:类型参数，用于表示任意类型
    E:元素类型，用于表示集合中的元素类型
    K:键类型，用于表示键值对中的键类型
    V:值类型，用于表示键值对中的值类型

    注意：
    不允许泛型实例化
    不允许创建数组 T[] arr = new T[10]; ❌
    
    */
    // list
    List<Integer> list = new ArrayList<>();

    //自定义泛型类
    class MyList<T> {
        private T content;
        // 构造方法
        public MyList(T content) {
            this.content = content;
        }
        // getter方法
        public T getContent() {
            return content;
        }
        public static void main(String[] args) {
            MyList<Integer> list = new MyList<>(10);
            System.out.println(list.getContent());
            // 10
            MyList<String> list2 = new MyList<>("hello");
            System.out.println(list2.getContent());
            // hello
        }
    }
    // 自定义交互方法的泛型
    public static <T> void swap(T a, T b) {
        T temp = a;
        a = b;
        b = temp;
    }
    // 自定义泛型接口
    interface MyComparator<k,v> {
        k getKey();
        v getValue();
    }
    //类型通配符，使用?表示未知类型，不能添加元素（除了null)，类型未知无法保证安全
    public static void print(List<?> list) {
        for (Object obj : list) {
            System.out.println(obj);
        }
    }
    //上界通配符:<? extends T> 表示类型必须是T的子类
    //下界通配符:<? super T> 表示类型必须是T或者T的父类


}