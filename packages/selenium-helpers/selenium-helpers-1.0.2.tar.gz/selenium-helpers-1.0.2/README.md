# selenium_helpers
Helpful utilities and wrappers for Selenium work.

There are two key utilities in here -

## Click
Used to resolve issues caused while clicking an element.
Very often, elements are overlayed in such a way that a click isn't as simple as it should be.

This addresses that; simple call it with -
```python
click(driver, element)
```


## Wait Until

Allows you to wait until some condition is met.

The following conditions are supported -

1. Title Is
2. Title Contains
3. URL Matches
4. URL Is
5. URL Contains
6. You Find
7. You Find All
8. You Find Text
9. You Find Button Text
10. You Find All Text
11. You Find Placeholder
12. You Don't Find

```python
wait_unti(driver, 'title is', 'Google')
```