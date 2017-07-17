# MonteBoo Virtual Observatory
## Munipack Artificial Sky

Pod umělohmotnou oblohou prší fotony, dopadají na listy funkcí roztroušených po křemíkovém poli. Jen pár vteřin trvající konvoluce, proti hodinám promarněných expozic. Plakáty na zdech a pivo pod schody. Kohout co kokrhá, když je čas jít spát. V rustikálním prostředí vzdáleného terminálu, za zataženou roletou, schoval jsem mezi řádky pointu dvojitého záporu v podmínce vložené do cyklu.

Pro tuhle srandičku budeš potřebovat ještě něco navíc než jen webový prohlížeč. Je mi jedno, kde ho vezmeš, jestli z distribučního repositáře `# apt-get install munipack`, jsi li sám si svým vlastním rootem, nebo z registru balíčků ve virtuálním prostředí `$ pip install flask`, ať tak nebo jak vyřeší se samy všechny závislosti. Na skoro všechno ostatní platí jednoduché, ale mocné zaklínadlo `./configure && make && sudo make install`. Pak už bude stačit jenom jeden *klon* a `cd` a můžeš si spustit vlastní server na lokále `$ python boo.py`. Pro ty co nechtějí být ničím rušeni, dovolím si doporučit

```bash
$ chromium --incognito --app=http://127.0.0.1:5000/404
```

![MonteBooVO](http://astrograzl.github.io/img/monteboovo.png)

