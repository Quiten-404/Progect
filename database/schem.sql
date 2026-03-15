-- Таблица категорий расходов
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,           -- Название категории
    description TEXT,                            -- Описание
    monthly_limit DECIMAL(10,2),                 -- Лимит на месяц (можно NULL)
);

-- Таблица расходов
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),  -- Сумма > 0
    expense_date DATE NOT NULL,                         -- Дата расхода
    description TEXT,                                    -- Описание
    category_id INTEGER NOT NULL,                        -- Категория
    payment_method VARCHAR(20) DEFAULT 'cash',          -- Способ оплаты
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Таблица доходов (опционально, для полной картины)
CREATE TABLE IF NOT EXISTS incomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    income_date DATE NOT NULL,
    source VARCHAR(100) NOT NULL,                -- Источник дохода
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для ускорения поиска
CREATE INDEX idx_expenses_date ON expenses(expense_date);
CREATE INDEX idx_expenses_category ON expenses(category_id);
CREATE INDEX idx_expenses_amount ON expenses(amount);
CREATE INDEX idx_categories_name ON categories(name);

-- Представление для статистики по дням
CREATE VIEW IF NOT EXISTS daily_stats AS
SELECT 
    expense_date,
    COUNT(*) as transactions_count,
    SUM(amount) as total_amount,
    AVG(amount) as average_amount
FROM expenses
GROUP BY expense_date;

-- Представление для статистики по категориям
CREATE VIEW IF NOT EXISTS category_stats AS
SELECT 
    c.id,
    c.name as category_name,
    COUNT(e.id) as expenses_count,
    SUM(e.amount) as total_amount,
    AVG(e.amount) as average_amount,
    c.monthly_limit,
    CASE 
        WHEN c.monthly_limit IS NOT NULL 
        THEN SUM(e.amount) * 100.0 / c.monthly_limit
        ELSE NULL
    END as budget_used_percent
FROM categories c
LEFT JOIN expenses e ON c.id = e.category_id
WHERE strftime('%Y-%m', e.expense_date) = strftime('%Y-%m', 'now')
GROUP BY c.id, c.name, c.monthly_limit;