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
}