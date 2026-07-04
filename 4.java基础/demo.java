import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;

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

          

}