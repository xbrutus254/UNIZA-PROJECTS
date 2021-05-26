/**
 * Write a description of class Pict here.
 * 
 * @author NightRain
 * @version 13-Nov-18
 */
public class Country {
    private String name;
    private int budget;
    private int population;
    private String relationshipWithYou;
    private int posX;
    private int posY;
    private int countOfMissile = 0;
    private int countOfAntiMissile = 0;
    /**
     * Constructor for objects of class Country
     * @param name budget population x y missile antimissile
     */
    public Country(String pName, int pBudget, int pPopulation, int x, int y, int miss, int antiMiss) {
        this.name = pName;
        this.budget = pBudget;
        this.population = pPopulation;
        this.relationshipWithYou = "neutral";
        this.posX = x;
        this.posY = y;
        this.countOfMissile = miss;
        this.countOfAntiMissile = antiMiss;
    }
    /*
    *  return counts of missiles
    *  @return count of missiles
    */
    public int getMissile() {
        return (this.countOfMissile);
    }
    /*
    *  return counts of anti missiles
    *  @return count of anti missiles
    */
    public int getAntiMissile() {
        return (this.countOfAntiMissile);
    }
    /*
    *  set counts of missiles
    *  @param missiles
    *  @return void
    */
    public void setMissile(int count) {
        this.countOfMissile = count;
    }
    /*
    *  set counts of anti missiles
    *  @param anti missiles
    *  @return void
    */
    public void setAntiMissile(int count) {
        this.countOfAntiMissile = count;
    }
    /*
    *  set money budget
    *  @param budget
    *  @return void
    */
    public void setBudget(int pBudget) {
        this.budget = pBudget;
    }
    /*
    *  set population of country
    *  @param population
    *  @return void
    */
    public void setPopulation(int pPopulation) {
        this.population = pPopulation;
    }
    /*
    *  return name of choosen country
    *  @return name
    */
    public String getName() {
        return (this.name);
    }
    /*
    *  get money budget
    *  @return budget
    */
    public int getBudget() {
        return (this.budget);
    }
    /*
    *  get population of choosen country
    *  @return population
    */
    public int getPopulation() {
        return (this.population);
    }
    /*
    *  get relationship that country keeps with u
    *  @return relationship
    */
    public String getRelationshipWithYou() {
        return (this.relationshipWithYou);
    }
    /*
    *  set relationship that country keeps with u
    *  @param change
    */
    public void setRelationshipWithYou(String change) {
        this.relationshipWithYou = change;
    }
    /*
    *  @return x
    */
    public int getPosX() {
        return (this.posX);
    }
    /*
    *  @return y
    */
    public int getPosY() {
        return (this.posY);
    }
    // unused method
    public String toString() {
        return ("Country: " + this.name + "\nBudget: " + this.budget + "\nPopulation: "
                + this.population);
    }
}
