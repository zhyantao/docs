# SOLID 五个原则

SOLID 原则是一组软件设计原则，用于指导软件开发人员设计和实现高质量的、易于维护和扩展的软件。它是由 Robert C. Martin 在其著作《Agile Software Development, Principles, Patterns, and Practices》中提出的，是目前软件工程界被广泛接受的一种软件设计理念。

## 1. 单一职责原则（SRP）

一个类别只应该有一个职责。也就是说，一个类别应该只有一个引起它变化的原因。以下范例表示，

```python
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.total = 0

    def add_item(self, item):
        self.items.append(item)
        self.total += item.price

    def remove_item(self, item):
        self.items.remove(item)
        self.total -= item.price

    def print_receipt(self):
        print('Items:')
        for item in self.items:
            print(f'{item.name} - ${item.price}')
        print(f'Total: ${self.total}')
```

这个 `ShoppingCart` 类别同时负责处理购物车相关的任务和输出相关的任务。它的 `print_receipt()` 方法应该被拆分为一个独立的类别或方法，以实现单一职责原则。

以下是改进后的代码：

```python
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.total = 0

    def add_item(self, item):
        self.items.append(item)
        self.total += item.price

    def remove_item(self, item):
        self.items.remove(item)
        self.total -= item.price

    def get_total(self):
        return self.total


class ReceiptPrinter:
    def print_receipt(self, shopping_cart):
        print('Items:')
        for item in shopping_cart.items:
            print(f'{item.name} - ${item.price}')
        print(f'Total: ${shopping_cart.get_total()}')


# 使用
shopping_cart = ShoppingCart()
# 假设 Item 类已经定义好了
item1 = Item("Product A", 10)
item2 = Item("Product B", 20)
shopping_cart.add_item(item1)
shopping_cart.add_item(item2)

receipt_printer = ReceiptPrinter()
receipt_printer.print_receipt(shopping_cart)
```

## 2. 开放封闭原则（OCP）

软件实体（类别、模组、函数等）应该对扩展开放，对修改封闭。这意味着当需要添加新功能时，应该扩展现有的实体，而不是修改它们。

```python
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def get_total_price(self):
        total_price = 0
        for item in self.items:
            total_price += item.price
        return total_price

class DiscountedShoppingCart(ShoppingCart):
    def get_total_price(self):
        total_price = super().get_total_price()
        return total_price * 0.9
```

在给出的代码中，`ShoppingCart` 类负责计算购物车中所有物品的总价。`DiscountedShoppingCart` 类继承了 `ShoppingCart` 并覆盖了 `get_total_price` 方法以应用折扣。这种实现方式违反了 OCP 原则，因为如果我们想要添加一个新的折扣策略，我们必须修改现有的 `DiscountedShoppingCart` 类，这可能会引入错误或破坏现有的功能。

为了遵循 OCP 原则，我们可以采用策略模式（Strategy Pattern），将不同的折扣策略封装在不同的类中，这样就可以通过增加新的策略类来扩展系统功能，而无需修改现有代码。

下面是改进后的代码示例：

```python
from abc import ABC, abstractmethod

# 抽象折扣策略接口
class IDiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, total_price):
        pass

# 无折扣策略
class NoDiscountStrategy(IDiscountStrategy):
    def apply_discount(self, total_price):
        return total_price

# 固定折扣策略
class FixedDiscountStrategy(IDiscountStrategy):
    def __init__(self, discount_rate):
        self.discount_rate = discount_rate

    def apply_discount(self, total_price):
        return total_price * self.discount_rate

# 购物车类
class ShoppingCart:
    def __init__(self, discount_strategy: IDiscountStrategy):
        self.items = []
        self.discount_strategy = discount_strategy

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def get_total_price(self):
        total_price = sum(item.price for item in self.items)
        return self.discount_strategy.apply_discount(total_price)

# 使用
item1 = Item("Product A", 10)
item2 = Item("Product B", 20)

# 创建购物车并应用固定折扣
discounted_cart = ShoppingCart(FixedDiscountStrategy(0.9))
discounted_cart.add_item(item1)
discounted_cart.add_item(item2)
print(discounted_cart.get_total_price())

# 创建购物车并应用无折扣
no_discount_cart = ShoppingCart(NoDiscountStrategy())
no_discount_cart.add_item(item1)
no_discount_cart.add_item(item2)
print(no_discount_cart.get_total_price())
```

在这个改进版本中，我们做了以下几点改变：

1. 定义了一个抽象类 `IDiscountStrategy`，它规定了应用折扣的接口。
2. 实现了两种具体的折扣策略：`NoDiscountStrategy` 和 `FixedDiscountStrategy`。
3. 修改了 `ShoppingCart` 类，使其接受一个 `IDiscountStrategy` 实例作为依赖，并在计算总价时应用该策略。

这样，如果我们想要添加新的折扣策略，只需实现 `IDiscountStrategy` 接口并创建一个新的策略类，然后将其传递给 `ShoppingCart` 即可，而无需修改现有的 `ShoppingCart` 类。这种方式遵循了 OCP 原则，使系统更加灵活和易于维护。

## 3. 里氏替换原则（LSP）

里氏替换原则描述的是子类应该能替换为它的基类。

意思是，给定 `class B` 是 `class A` 的子类，在预期传入 `class A` 的对象的任何方法传入 `class B` 的对象，方法都不应该有异常。

这是一个预期的行为，因为继承假定子类继承了父类的一切。子类可以扩展行为但不会收窄。

因此，当 `class` 违背这一原则时，会导致一些难于发现的讨厌的 bug。

里氏替换原则容易理解但是很难在代码里发现。看一个例子：

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def area(self):
        return self.width * self.height

class Square(Rectangle):
    def __init__(self, size):
        self.width = size
        self.height = size

    def set_width(self, width):
        self.width = width
        self.height = width

    def set_height(self, height):
        self.width = height
        self.height = height

square = Square(5)
square.set_width(10)
square.set_height(5)
print(square.area())
```

在给出的代码中，`Square` 类继承自 `Rectangle` 类。然而，`Square` 类重写了 `set_width` 和 `set_height` 方法，使得设置宽度或高度时会同时改变另一个维度，以保持正方形的特性（即宽度和高度相等）。

当我们在代码中这样使用 `Square` 类时：

```python
square = Square(5)
square.set_width(10)
square.set_height(5)
print(square.area())
```

我们期望得到的结果是正方形的面积，但是由于 `Square` 类的特殊性质，当我们先设置宽度为 10，再设置高度为 5 时，`Square` 类会将宽度也设置为 5。因此，最终的面积将是 5 _ 5 = 25，而不是预期的 10 _ 5 = 50。

这个问题违反了 LSP 原则，因为在 `Rectangle` 类中，我们可以分别设置宽度和高度，但在 `Square` 类中这样做会导致意外的行为。这破坏了基类和子类之间的一致性，因为 `Square` 类不能被用来替代 `Rectangle` 类，尤其是在期望宽度和高度可以独立变化的情况下。

为了遵循 LSP 原则，我们可以采取以下方法来解决这个问题：

```python
class Shape:
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def area(self):
        return self.width * self.height

class Square(Shape):
    def __init__(self, size):
        self.size = size

    def set_size(self, size):
        self.size = size

    def area(self):
        return self.size ** 2

def print_area(shape):
    print(f"Area: {shape.area()}")

shapes = [Rectangle(5, 10), Square(5)]
for shape in shapes:
    print_area(shape)
```

在这个改进后的代码中，`Rectangle` 和 `Square` 类都继承自 `Shape` 类，并实现了 `area` 方法。这样，无论是 `Rectangle` 还是 `Square`，都可以作为 `Shape` 的实例使用，并且 `print_area` 函数可以正确地调用它们各自的 `area` 方法。由于 `Square` 类不再继承自 `Rectangle` 类，所以不会出现 `Square` 类中宽度和高度相互影响的问题。

通过这种方式，我们确保了 `Rectangle` 和 `Square` 类可以互相替换，并且在替换后程序的行为不会发生改变，因此解决了 LSP 的问题。

## 4. 接口隔离原则（ISP）

隔离意味着保持独立，接口隔离原则是关于接口的独立。

该原则描述了很多客户端特定的接口优于一个多用途接口。客户端不应该强制实现他们不需要的函数。

这是一个简单的原则，很好理解和实践，直接看例子。

先来看一段违反 ISP 的代码：

```python
class Machine:
    def print(self, document):
        pass

    def fax(self, document):
        pass

    def scan(self, document):
        pass

class MultiFunctionPrinter(Machine):
    def print(self, document):
        print("Printing")

    def fax(self, document):
        print("Faxing")

    def scan(self, document):
        print("Scanning")
```

在提供的代码中，`Machine` 类定义了三个方法：`print`、`fax` 和 `scan`。然后 `MultiFunctionPrinter` 类继承了 `Machine` 类，并实现了这三个方法。如果存在一些打印机只支持打印功能而不支持传真或扫描，那么这些打印机就需要实现一个它们实际上并不需要的接口，这就违反了 ISP 原则。

例如，假设我们有一个仅支持打印功能的类 `Printer`，它也需要从 `Machine` 继承，那么它将被迫实现 `fax` 和 `scan` 方法，即使它实际上并不使用这些功能。这会导致代码冗余并且难以维护。

为了遵循 ISP 原则，我们可以将 `Machine` 类分解为更小、更具体的接口，例如 `Printer`, `Scanner`, 和 `FaxMachine`，这样只有那些真正需要这些功能的子类才会去实现它们。这里是一个改进后的例子：

```python
class Printer:
    def print(self, document):
        pass

class Scanner:
    def scan(self, document):
        pass

class FaxMachine:
    def fax(self, document):
        pass

class MultiFunctionPrinter(Printer, Scanner, FaxMachine):
    def print(self, document):
        print("Printing")

    def fax(self, document):
        print("Faxing")

    def scan(self, document):
        print("Scanning")

class SimplePrinter(Printer):
    def print(self, document):
        print("Printing")
```

在这个例子中，`SimplePrinter` 只实现了打印功能，而 `MultiFunctionPrinter` 实现了所有三种功能。这样，每个类都只需要关心自己需要的功能，从而更好地遵循了 ISP 原则。

## 5. 依赖反转原则（DIP）

依赖倒置原则描述的是我们的 `class` 应该依赖接口和抽象类而不是具体的类和函数。

在这篇[文章](https://fi.ort.edu.uy/innovaportal/file/2032/1/design_principles.pdf)（2000）里，Bob 大叔如下总结该原则：

> 如果 OCP 声明了 OO 体系结构的目标，那么 DIP 则声明了主要机制。

这两个原则的确息息相关，我们在讨论开闭原则之前也要用到这一模式。

我们想要我们的类开放扩展，因此我们需要明确我们的依赖的是接口而不是具体的类。我们的 `PersistenceManager` 类依赖 `InvoicePersistence` 而不是实现了这个接口的类。

先来看一个错误的范例：

```python
class Logger:
    def log(self, message):
        print(f"Log: {message}")

class UserService:
    def __init__(self):
        self.logger = Logger()

    def register(self, username, password):
        try:
            # register user to database
            print(f"User {username} registered successfully")
            self.logger.log(f"User {username} registered successfully")
        except Exception as e:
            print(f"Error: {e}")
            self.logger.log(f"Error: {e}")
```

根据 DIP，高层次模块不应该依赖于低层次模块，而应该依赖于抽象；抽象不应该依赖于细节，细节应该依赖于抽象。

在这段代码中，`UserService` 类直接创建了一个 `Logger` 实例并使用它，这导致了几个问题：

1. **直接依赖于具体实现**：`UserService` 直接依赖于 `Logger` 类的具体实现。这意味着如果 `Logger` 类的行为发生变化，或者我们想要更换不同的日志记录机制（比如从控制台输出改为文件记录），`UserService` 类也需要进行相应的修改。
2. **紧密耦合**：`UserService` 和 `Logger` 之间形成了紧密的耦合，这使得它们很难独立地进行单元测试，也增加了代码的维护成本。

为了遵循 DIP，我们应该将 `Logger` 的行为抽象出来，并通过依赖注入的方式将具体的实现传入 `UserService`。这样可以确保 `UserService` 只依赖于抽象，并且可以很容易地替换 `Logger` 的实现。

下面是一个改进的例子：

```python
from abc import ABC, abstractmethod

# 定义一个抽象的日志接口
class ILogger(ABC):
    @abstractmethod
    def log(self, message):
        pass

# 具体的日志实现
class ConsoleLogger(ILogger):
    def log(self, message):
        print(f"Log: {message}")

# 用户服务类现在依赖于抽象的日志接口
class UserService:
    def __init__(self, logger: ILogger):
        self.logger = logger

    def register(self, username, password):
        try:
            # register user to database
            print(f"User {username} registered successfully")
            self.logger.log(f"User {username} registered successfully")
        except Exception as e:
            print(f"Error: {e}")
            self.logger.log(f"Error: {e}")

# 使用
console_logger = ConsoleLogger()
user_service = UserService(console_logger)
user_service.register("john_doe", "securepassword")
```

在这个改进版本中，我们做了以下改变：

- 创建了一个抽象基类 `ILogger`，定义了 `log` 方法。
- `ConsoleLogger` 类实现了 `ILogger` 接口。
- `UserService` 类不再直接创建 `Logger` 实例，而是通过构造函数接收一个 `ILogger` 对象作为依赖。
- 当创建 `UserService` 实例时，我们传入了一个具体的 `ConsoleLogger` 实例。

这样，`UserService` 类只依赖于抽象的 `ILogger` 接口，而具体的实现（例如 `ConsoleLogger`）可以通过依赖注入的方式提供，这使得整个系统更加灵活、可测试和易于维护。
