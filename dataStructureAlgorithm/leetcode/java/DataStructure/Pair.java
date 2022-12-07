package DataStructure;

public class Pair<K,V>
{
    public K x;
    public V y;

    public Pair(K x, V y)
    {
        this.x = x;
        this.y = y;
    }

    @Override
    public boolean equals(Object o)
    {
        if(this == o) return true;
        if(o==null || getClass() != o.getClass()) return false;

        // Convert o to Pair Object

        Pair<?,?> pair = (Pair<?, ?>) o;

        // Compare key and value

        if(!x.equals(pair.x)) return false;
        return y.equals(pair.y);
    }

    @Override
    public int hashCode()
    {
        return 31* x.hashCode()+ y.hashCode();
    }

    // Factory method for creating immutable Pairs
    // I will make this Pair class mutable, so this is not really needed

    /*
    public static <K,V> Pair <K,V> of(K key, V value)
    {
        return new Pair<>(key,value);
    }
     */

}
