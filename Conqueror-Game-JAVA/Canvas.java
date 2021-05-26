import javax.swing.JFrame;
import javax.swing.JLabel;
import java.awt.event.*;  
import java.awt.*; 
import javax.swing.*;
import java.util.ArrayList;

import javax.swing.Icon;

import javax.swing.ImageIcon;
import javax.swing.JFrame;
import java.util.Random;

import java.util.Timer;
import java.util.TimerTask;

/**
 * Write a description of class Pict here.
 * 
 * @author NightRain
 * @version 13-Nov-18
 */

public class Canvas extends JFrame  {
    private ArrayList<Country> countries;
    private int selectedX = 220;
    private int selectedY = 320;
    private int myPosX = 0;
    private int myPosY = 0;
    private int tempX = 0;
    private int tempY = 0;
    private int missile = 0;
    private int antiMissile = 0;
    private String nameOfMyCountry = "";
    private String nameOfChoosenCountry = "";
    private int lengthX = 0; // distance between your country and enemy
    private int lengthMedium = 0;
    private int lengthY = 0;
    private int step = 0;

    // fixed objects for each country
    private Country algeria;
    private Country libya;
    private Country egypt;
    private Country saudiArabia;
    private Country iraq;
    private Country syria;
    private Country iran;
    private Country afghanistan;
    private Country turkey;
    private Country turkmenistan;
    private Country uzbekistan;
    private Country kazakhstan;
    private Country ukraine;
    private Country belarus;
    private Country poland;
    private Country romania;
    private Country bulgaria;
    private Country greece ;
    private Country balkania;
    private Country hungary;
    private Country austria;
    private Country slovakia;
    private Country czechRep;
    private Country germany;
    private Country italy;
    private Country france;
    private Country unitedKingdom;
    private Country ireland;
    private Country spain;
    private Country portugal;
    private Country morocco;

    public Canvas(int countryNum) {

        this.countries = new ArrayList<Country>();
        /*
         *  Create countries
         */
        this.createCountries();

        JLabel image;
        Icon line1;
        Icon line2;
        String yourCountry = "";
        line1 = new ImageIcon("data/line.png");
        line2 = new ImageIcon("data/line.png");
        //**********************************************//
        /*
         *  load image
         */
        if (countryNum == 1) {
            image = new JLabel(new ImageIcon("data/mapALGERY.jpg"));
            yourCountry = "Algeria";
        } else if (countryNum == 2) {
            image = new JLabel(new ImageIcon("data/mapD.jpg"));
            yourCountry = "Germany";
        } else if (countryNum == 3) {
            image = new JLabel(new ImageIcon("data/mapFR.jpg"));
            yourCountry = "France";
        } else if (countryNum == 4) {
            image = new JLabel(new ImageIcon("data/mapIRAN.jpg"));
            yourCountry = "Iran";
        } else if (countryNum == 5) {
            image = new JLabel(new ImageIcon("data/mapKazach.jpg"));
            yourCountry = "Kazakhstan";
        } else if (countryNum == 6) {
            image = new JLabel(new ImageIcon("data/mapPL.jpg"));
            yourCountry = "Poland";
        } else if (countryNum == 7) {
            image = new JLabel(new ImageIcon("data/mapSaudiAr.jpg"));
            yourCountry = "Saudi_Arabia";
        } else if (countryNum == 8) {
            image = new JLabel(new ImageIcon("data/mapSK.jpg"));
            yourCountry = "Slovakia";
        } else {
            return;
        }
        this.nameOfMyCountry = yourCountry;
        JLabel myCountryLabel = new JLabel(yourCountry); // my country label 

        JButton showComboLabel = new JButton("Show");  // BUTTON IMAGE 
        JButton showComboLabelBuyAM = new JButton("Buy AM");
        JButton showComboLabelBuyDM = new JButton("Buy DM");
        JButton line1Buttom = new JButton(line1);      // Image uploaded to button
        JButton line2Buttom = new JButton(line2);      // Image uploaded to button
        JButton missileButtom = new JButton("FIRE");      // Image uploaded to button
        JButton exitButton = new JButton("End SMBS");
        JButton nextButton = new JButton("NEXT STEP");
        // array of states
        String[] country = {"Algeria", "Libya", "Egypt", "SaudiArabia", "Iraq" + 
                "", "Iran", "Syria", "Turkmenistan", "Uzbekistan", "Kazakhstan" + 
                "", "Afghanistan", "Turkey", "Ukraine", "Belarus", "Poland" + 
                "", "Germany", "France", "CzechRepub", "Slovakia", "Romania" + 
                "", "Hungary", "Austria", "Bulgaria", "Greece", "Balkania", "Italy" + 
                "", "Spain", "Portugal", "UnitedKingdom", "Ireland", "Morocco"};   
        String[] aM = {"1x  -    420,000 $", "2x  -    820,000 $", "5x   -  2,100,000 $", "10x - 4,200,000 $", "20x - 8,400,000 $"}; 
        String[] dM = {"1x  -    280,000 $", "2x  -    560,000 $", "5x   -  1,400,000 $", "10x - 2,800,000 $", "20x - 5,600,000 $"};

        JComboBox box = new JComboBox(country);  // BOX OF STATES   
        JComboBox boxBuyAM = new JComboBox(aM);  // BOX OF STATES   
        JComboBox boxBuyDM = new JComboBox(dM);  // BOX OF STATES   
        String selectedCountryString = ("Selected country: ");      // string 
        String yourCountryPat = ("Your Country Info: ");            // string 
        //----------------------------------------------------------//

        JLabel infoChoosedCountryLabel = new JLabel(); //  Selected country: "create"
        JLabel infoCountryLabel = new JLabel();        //  Your Country:     "create"

        infoChoosedCountryLabel.setText(selectedCountryString); // 'select country' label
        infoCountryLabel.setText(yourCountryPat);               // 'Your country info' label

        JLabel infoChoosedCountryLabel2 = new JLabel();
        infoChoosedCountryLabel2.setText(yourCountry);      // 'Germany' <- top bottom label

        JLabel stepLabel = new JLabel();
        stepLabel.setText("STEP : 0");      // step <- top bottom label

        JLabel altitudeInfoLabel = new JLabel();
        altitudeInfoLabel.setText("CALIBRATED ALTITUDE: 0");      // altitude

        JLabel speedInfoLabel = new JLabel();
        speedInfoLabel.setText("GROUND SPEED:        0");      // speed

        //************************ MY COUNTRY *************************//
        int[] myList;                           
        myList = new int[3];
        myList = this.getParameters(yourCountry);       // <- Budget + Population + posX + posY
        String budg = exactFormatValue(myList[0]); // Budget     
        String popul = exactFormatValue(myList[1]);     // Population
        this.myPosX = myList[2];                        // pos X
        this.myPosY = myList[3];                        // posY
        this.missile = myList[4];
        this.antiMissile = myList[5];
        //-----------------------------------------------------------//

        JLabel infoMissileLabel = new JLabel("Attack Missile:   " + this.missile);
        JLabel infoAntiMissileLabel = new JLabel("Defense Missile: " + this.missile);
        JLabel inforealtLabel = new JLabel("Realtionship: "); // relationship
        JLabel infoBudgetLabel2 = new JLabel("Budget:        " + budg + "$"); // budget

        JLabel infoPopulationLabel = new JLabel("Population: ");
        JLabel infoPopulationLabel2 = new JLabel("Population: " + popul);

        //-----------------------------------------------------------//
        // BUY ATTACK MISSILES
        showComboLabelBuyAM.addActionListener(new ActionListener() {  
                public void actionPerformed(ActionEvent e) {   
                    String data = "" + boxBuyAM.getItemAt(boxBuyAM.getSelectedIndex());      // list of MY country parameters
                    int missile = 0;
                    int budg = 0;
                    // choose quantity
                    if (data.equals("1x  -    420,000 $")) {
                        missile = 1;
                        budg = 420000;
                    } else if (data.equals("2x  -    820,000 $")) {
                        missile = 2;
                        budg = 820000;
                    } else if (data.equals("5x   -  2,100,000 $")) {
                        missile = 5;
                        budg = 2100000;
                    } else if (data.equals("10x - 4,200,000 $")) {
                        missile = 10;
                        budg = 4200000;
                    } else if (data.equals("20x - 8,400,000 $")) {
                        missile = 20;
                        budg = 8400000;
                    }
                    // if is lower than budget, continue
                    if (checkBudget(budg, nameOfMyCountry)) {
                        decBudget(budg, nameOfMyCountry); // sub bbudget
                        setMiss(missile, nameOfMyCountry); // add missiles
                        // "Budget:        " + exactFormatValue(getBudget(nameOfMyCountry)) + "$"
                        // set new labels info
                        infoBudgetLabel2.setText("Budget:        " + exactFormatValue(getBudget(nameOfMyCountry)) + "$"); // moj budget
                        infoMissileLabel.setText("Attack Missile:   " + Integer.toString(getMiss(nameOfMyCountry)));
                    }
                }  
            }); 
        //-----------------------------------------------------------//
        // BUY DEFFENCE MISSILES
        showComboLabelBuyDM.addActionListener(new ActionListener() {  
                public void actionPerformed(ActionEvent e) {   
                    String data = "" + boxBuyDM.getItemAt(boxBuyDM.getSelectedIndex());      // list of MY country parameters
                    int missile = 0;
                    int budg = 0;
                    if (data.equals("1x  -    280,000 $")) {
                        missile = 1;
                        budg = 280000;
                    } else if (data.equals("2x  -    560,000 $")) {
                        missile = 2;
                        budg = 560000;
                    } else if (data.equals("5x   -  1,400,000 $")) {
                        missile = 5;
                        budg = 1400000;
                    } else if (data.equals("10x - 2,800,000 $")) {
                        missile = 10;
                        budg = 2800000;
                    } else if (data.equals("20x - 5,600,000 $")) {
                        missile = 20;
                        budg = 5600000;
                    }
                    if (checkBudget(budg, nameOfMyCountry)) {
                        decBudget(budg, nameOfMyCountry);
                        setAntiMiss(missile, nameOfMyCountry);

                        infoBudgetLabel2.setText("Budget:        " + exactFormatValue(getBudget(nameOfMyCountry)) + "$"); // moj budget
                        infoAntiMissileLabel.setText("Defense Missile: " + Integer.toString(getAntiMiss(nameOfMyCountry)));
                    }
                }  
            }); 
        //-----------------------------------------------------------//
        // ********************* COMBO SELECT *********//
        showComboLabel.addActionListener(new ActionListener() {  
                public void actionPerformed(ActionEvent e) {   
                    int[] myList2;        // list of choosed country parameters
                    myList2 = new int[3]; // list of my country parameters

                    String data2 = "" + box.getItemAt(box.getSelectedIndex());      // list of MY country parameters
                    infoChoosedCountryLabel2.setText(data2);

                    String text = infoChoosedCountryLabel2.getText();
                    nameOfChoosenCountry = text;
                    myList2 = getParameters(text);
                    String relat = getRealtionship(text);
                    String popul = exactFormatValue(myList2[1]);
                    selectedX = myList2[2];
                    selectedY = myList2[3];

                    String data3 = "Realtionship: " + box.getItemAt(box.getSelectedIndex());  
                    inforealtLabel.setText("Relationship: " + relat);
                    String data4 = "Population:  " + box.getItemAt(box.getSelectedIndex());  
                    infoPopulationLabel.setText("Population:  " + popul);                
                }  
            });  

        //  Boarders
        //--------------------------------------//

        image.setBounds(10, 10, 1000, 500);          // MAP
        line1Buttom.setBounds(250, 510, 5, 290);
        line2Buttom.setBounds(790, 510, 5, 290);
        infoChoosedCountryLabel.setBounds(20, 515, 150, 30); // Select country
        infoCountryLabel.setBounds(800, 515, 150, 30);       // Param MY country
        stepLabel.setBounds(170, 745, 150, 40);

        boxBuyAM.setBounds(530, 550, 150, 30);                    // MagicBox
        boxBuyDM.setBounds(530, 585, 150, 30);                    // MagicBox
        showComboLabelBuyAM.setBounds(680, 550, 100, 30);
        showComboLabelBuyDM.setBounds(680, 585, 100, 30);

        box.setBounds(20, 550, 150, 30);                    // MagicBox
        inforealtLabel.setBounds(20, 600, 150, 30);         // BUDGET label
        infoPopulationLabel.setBounds(20, 635, 150, 30);     // POPULATION label

        infoMissileLabel.setBounds(800, 575, 150, 30);
        infoAntiMissileLabel.setBounds(800, 595, 150, 30);
        infoBudgetLabel2.setBounds(800, 615, 150, 30);         // MY BUDGET label
        infoPopulationLabel2.setBounds(800, 635, 150, 30);     // MY POPULATION label

        myCountryLabel.setBounds(483, 700, 90, 20);          // Top Bottom Name
        showComboLabel.setBounds(170, 550, 75, 30);          // BUTTON SHOW
        //--------------------------------------//
        JLabel missile = new JLabel(new ImageIcon("data/rocket.png"));
        missile.setBounds(450, 600, 20, 20);
        missileButtom.setBounds(680, 650, 100, 50);
        exitButton.setBounds(940, 745, 100, 50);
        nextButton.setBounds(5, 745, 100, 50);

        altitudeInfoLabel.setBounds(260, 550, 200, 30);
        speedInfoLabel.setBounds(260, 585, 200, 30);

        //--------------------------------------//
        ImageIcon img = new ImageIcon("data/nuclear.png");
        this.setIconImage(img.getImage());

        //  ADDONS
        //--------------------------------------//
        this.add(line1Buttom);
        this.add(line2Buttom);
        this.add(image);
        this.add(infoChoosedCountryLabel);
        this.add(infoCountryLabel);
        this.add(stepLabel);
        this.add(box);
        this.add(inforealtLabel);
        this.add(infoPopulationLabel);
        this.add(infoBudgetLabel2);
        this.add(infoPopulationLabel2);

        this.add(infoMissileLabel);
        this.add(infoAntiMissileLabel);

        this.add(myCountryLabel);
        this.add(showComboLabel);
        //------------------------------//
        // ADD BUY
        this.add(boxBuyAM);
        this.add(boxBuyDM);
        this.add(showComboLabelBuyAM);
        this.add(showComboLabelBuyDM);

        //------------------------------//
        // Missile altitude and speed

        this.add(altitudeInfoLabel);
        this.add(speedInfoLabel);

        //this.add(missile);
        //--------------------------------------//
        this.add(missileButtom); 
        this.add(exitButton);
        this.add(nextButton);
        missile.setBounds(myPosX, myPosY, 25, 25); 
        add(missile); 
        add(image);
        // ********************* NEXT STEP *********//
        nextButton.addActionListener (new ActionListener() {  
                public void actionPerformed(ActionEvent e) {  
                    setPopulationByKoef();
                    int[] myList;                           
                    myList = new int[3];
                    myList = getParameters(nameOfMyCountry);       // <- Budget + Population + posX + posY
                    String budg = exactFormatValue(myList[0]); // Budget     
                    String popul = exactFormatValue(myList[1]);     // Population
                    infoBudgetLabel2.setText("Budget:        " + budg + "$"); // moj budget
                    infoPopulationLabel2.setText("Population: " + popul);
                    step++;
                    stepLabel.setText("STEP : " + exactFormatValue(step)); // step

                    int enemPop = getPopulation(nameOfChoosenCountry);
                    infoPopulationLabel.setText("Population:  " + exactFormatValue(enemPop)); 
                    //-------------------------------
                    int newMyPop = randWar();
                    randBudgPop();
                    otherCountriesBuyMissiles();
                    popul = exactFormatValue(newMyPop);     // Population
                    //infoPopulationLabel2.setText("Population: " + popul);

                    // TODO enemy attack
                    //************************ MY COUNTRY *************************//

                    myList = getParameters(nameOfMyCountry);       // <- Budget + Population + posX + posY
                    popul = exactFormatValue(myList[1]);     // Population
                    antiMissile = myList[5];
                    //-----------------------------------------------------------//

                    infoAntiMissileLabel.setText("Defense Missile: " + antiMissile);
                    JLabel infoPopulationLabel2 = new JLabel("Population: " + popul);
                    System.out.println("---------------------------------------");

                    if (myList[1] == 0) { // if all people of your country die
                        System.out.println(">> YOU BURNT! ALL YOUR PEOPLE DIED");
                        System.out.println(">> ------- GAME OVER! -------");
                        System.exit(0);
                    }
                    // --------------------------------
                }
            });
        // ********************* END *********//
        exitButton.addActionListener (new ActionListener() {  
                public void actionPerformed(ActionEvent e) {  
                    System.exit(0);
                }
            });
        // ********************* FIRE *********//
        missileButtom.addActionListener(new ActionListener() {  
                public void actionPerformed(ActionEvent e) {  
                    tempX = myPosX; // my positions
                    tempY = myPosY;
                    //---------------------// distance of X
                    //int lengthX = 0; 
                    if (tempX < selectedX) {
                        lengthX = selectedX - tempX;
                    } else if (tempX > selectedX)  {
                        lengthX = tempX - selectedX;
                    } else {
                        lengthX = selectedX;
                    }
                    //---------------------// distance of Y
                    //int lengthY = 0; 
                    if (tempY < selectedY) {
                        lengthY = selectedY - tempY;
                    } else if (tempX > selectedX) {
                        lengthY = tempY - selectedY;
                    } else {
                        lengthY = selectedY;
                    }
                    if (lengthX < lengthY) { 
                        lengthMedium = lengthY;
                    } else {
                        lengthMedium = lengthX;
                    }

                    //---------------------// 

                    Timer timer = new Timer();
                    missile.setBounds(tempX, tempY, 30, 30); 
                    Point pt = missile.getLocation();

                    if (getMiss(nameOfMyCountry) == 0) {
                        System.out.println(">> No missiles!");
                        return;
                    }

                    // if my country
                    if (tempX == selectedX && tempY == selectedY) {
                        System.out.println(">> You betrayed your country!");
                        System.exit(-1);
                    }

                    timer.schedule(new TimerTask() {
                            private int i = 0;
                            private double speedUp = lengthMedium * 0.8;
                            private int speed = 0;
                            private double speedDown = lengthMedium * 0.05;
                            private double altitudeUp = lengthMedium * 0.6;
                            private int altitude = 0;
                            private double altitudeDown = lengthMedium * 0.3;

                            @Override
                            public void run() {
                                Random rand = new Random();
                                int n = 0;
                                /*
                                 * i++;
                                System.out.println("--------------- " + i);
                                System.out.println("Moja X: " + tempX);
                                System.out.println("Moja Y: " + tempY);
                                System.out.println("Jeho X: " + selectedX);
                                System.out.println("Jeho Y: " + selectedY); 
                                 */
                                if (lengthMedium > altitudeUp && altitude < 50000) {
                                    n = rand.nextInt(450) + 315;
                                    altitude += n;
                                } else if (altitudeUp > lengthMedium && lengthMedium > altitudeDown) {
                                    n = rand.nextInt(3) - 1;
                                    altitude += n;
                                } else {
                                    n = rand.nextInt(6125) + 5125;
                                    altitude -= n;
                                    if (altitude <= 100) {
                                        altitude = 1245;
                                    }
                                }
                                if (lengthMedium > speedUp && speed < 5000 ) {
                                    n = rand.nextInt(50) + 35;
                                    speed += n;
                                } else if (speedUp > lengthMedium && lengthMedium > speedDown) {
                                    n = rand.nextInt(3) - 1;
                                    speed += n;
                                } else {
                                    n = rand.nextInt(20) + 7;
                                    speed -= n;
                                }
                                // changing coordinates
                                if (tempX < selectedX) {
                                    tempX++;
                                } else if (tempX > selectedX) {
                                    tempX--;
                                } else {
                                    tempX = selectedX;
                                }
                                if (tempY < selectedY) {
                                    tempY++;
                                } else if (tempY > selectedY) {
                                    tempY--;
                                } else {
                                    tempY = selectedY;
                                }
                                // *********************************************** // 
                                String result = exactFormatValue(altitude);
                                altitudeInfoLabel.setText("CALIBRATED ALTITUDE:  " + result + " m");      // altitude
                                result = exactFormatValue(speed);
                                speedInfoLabel.setText("GROUND SPEED:         " + result + " km/h");      // speed

                                lengthMedium--;
                                // -------------------------------- if hit
                                missile.setLocation(tempX, tempY);
                                if (tempX == selectedX && tempY == selectedY) {
                                    int[] fockList;
                                    fockList = new int[3];

                                    changeRelationShip();
                                    setMiss(-1, nameOfMyCountry);
                                    infoMissileLabel.setText("Attack Missile:  " + Integer.toString(getMiss(nameOfMyCountry)));

                                    fockList =  defence(nameOfChoosenCountry, nameOfMyCountry);
                                    int myPopulation = fockList[0];
                                    String regularPop = exactFormatValue(myPopulation);

                                    infoPopulationLabel2.setText("Population: " + regularPop);
                                    int enemyPopulation = fockList[1];
                                    regularPop = exactFormatValue(enemyPopulation);

                                    infoPopulationLabel.setText("Population:   " + regularPop);
                                    String atwar = "At war!";
                                    inforealtLabel.setText("Relationship: " + atwar);
                                    System.out.println("---------------------------------------");
                                    speedInfoLabel.setText("GROUND SPEED:        0 km/h");      // speed
                                    altitudeInfoLabel.setText("CALIBRATED ALTITUDE:  0 m");      // altitude
                                    timer.cancel();
                                }
                            }
                        }, 0, 50);
                    //changeRelationShip();
                }
            });

        //--------------------------------------//
        this.setUndecorated(true);
        this.setBackground(new Color(0.55f, 1.0f, 0.55f, 0.8f));
        this.setLayout(null);
        this.setSize(1045, 800);
        this.setVisible(true);
        this.setLocationRelativeTo(null); 
        this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        ///////////////////////////////////////////////

    }
    // ------------------------------------------------//
    /*
     *  method what make other countries to buy a missiles
     *  @param text
     *  @return void 
     */
    public void otherCountriesBuyMissiles() {
        Random rand = new Random();
        int budg = 0;
        int n = 0;
        int count = 0;
        int attackM = 0;
        int deffM = 0;

        for (Country aktualna : this.countries) {
            if (aktualna.getName().equals(nameOfMyCountry)) {
                continue;
            }
            budg = aktualna.getBudget();
            if (budg < 280000) {
                continue;
            } else if (budg < 560000) {
                attackM = 1;
                deffM = 2;
            } else if (budg < 1400000) {
                attackM = 3;
                deffM = 5;
            } else if (budg < 2100000) {
                attackM = 5;
                deffM = 7;
            } 
            attackM = rand.nextInt((attackM - 0) + 1) + 0;
            deffM = rand.nextInt((deffM - 0) + 1) + 0;

            if (checkBudget(attackM * 420000, aktualna.getName()) && attackM != 0) {
                decBudget(attackM * 420000, aktualna.getName());
                setAntiMiss(attackM, aktualna.getName());
                //System.out.println(aktualna.getName() + " buying " + attackM + " attackM");
            }

            if (checkBudget(deffM * 420000, aktualna.getName()) && deffM != 0) {
                decBudget(deffM * 280000, aktualna.getName());
                setAntiMiss(deffM, aktualna.getName());
                //System.out.println(aktualna.getName() + " buying " + deffM + " deffM");
            }
            //System.out.println("Budget of " + aktualna.getName() + " : " + aktualna.getBudget());
        }
    }
    // ------------------------------------------------//
    /*
     *  add budget and popualtion to other countries
     *  @return void 
     */
    public void randBudgPop() {
        int actPop = 0;
        int actBudg = 0;
        int randAddBudg = 0;
        double min = 0;
        double max = 0;
        double n = 0;
        for (Country aktualna : this.countries) {
            actPop = aktualna.getPopulation();
            max = actPop * 0.35;
            min = actPop * 0.1;
            //n = rand.nextDouble(max) + min;
            //n = min + (n * (max - min));
            n = min + new Random().nextDouble() * (max - min);
            aktualna.setPopulation(actPop + (int)n);
            //----------------------------------------------------//
            actBudg = aktualna.getBudget();
            actPop = aktualna.getPopulation();
            n = actPop * 0.03;
            aktualna.setBudget(actBudg + (int)n);

        }
    }
    // ------------------------------------------------//
    /*
     *  countries declare war due to relat. with you
     *  make war to you
     *  @return int 
     */
    public int randWar() {
        Random rand = new Random();
        int[] fockList;
        fockList = new int[3];
        int mypop = getPopulation(nameOfMyCountry);

        for (Country aktualna : this.countries) {
            if (aktualna.getPopulation() == 0) {
                continue;
            }
            if (aktualna.getRelationshipWithYou().equals("At war!")) {
                int n = rand.nextInt(10) + 1;
                if (n > 5 && aktualna.getMissile() >= 1) {
                    System.out.println(">> " + aktualna.getName() + " Starting attack!");
                    fockList =  defence(nameOfMyCountry, aktualna.getName());

                    setMiss(-1, aktualna.getName());
                    mypop = fockList[0];
                    //String regularPop = exactFormatValue(myPopulation);

                    //infoPopulationLabel2.setText("Population: " + regularPop);

                }
            } else {
                int n = rand.nextInt(100) + 1;
                if (n > 98 && !aktualna.getName().equals(nameOfMyCountry)) {
                    aktualna.setRelationshipWithYou("At war!");
                    System.out.println(">> " + aktualna.getName() + " declares war at you!");
                }
            }
        }
        return mypop;
    }
    // -------------------------------------------------//
    /*
     *  return true if inserted budget is lower than actual
     *  @param budg country
     *  @return boolean 
     */
    public Boolean checkBudget(int budg, String country) {
        Boolean ifTrue = true;
        for (Country aktualna : this.countries) {
            if (aktualna.getName().equals(country)) {
                if (budg > aktualna.getBudget()) {
                    return false;
                } else {
                    return true;
                }
            }         
        }
        return ifTrue;
    }
    // -------------------------------------------------// 
    /*
     *  set budget actual - paramBudget
     *  @param country count
     *  @return void 
     */
    public void decBudget(int count, String country) {
        int budg = 0;
        for (Country aktualna : this.countries) {
            if (aktualna.getName().equals(country)) {
                budg = aktualna.getBudget();
                if (this.checkBudget(count, country)) {
                    aktualna.setBudget(budg - count);
                }    
                //System.out.println(">> " + aktualna.getMissile());
            }         
        }
    }
    // -------------------------------------------------//
    /*
     *  return value of actual budget
     *  @param country
     *  @return int
     */
    public int getBudget(String country) {
        int budg = 0;
        for (Country aktualna : this.countries) {
            if (aktualna.getName().equals(country)) {
                budg = aktualna.getBudget();  
            }         
        }
        return budg;
    }
    // -------------------------------------------------//
    /*
     *  return readable format of number in string
     */
    public String exactFormatValue(int value) {
        String regularPop = Integer.toString(value); // 123456
        int length = regularPop.length();            // 6
        int realLength = length;                    // 6
        int modular = length % 3;    // 0
        int pointer = modular;      // 0

        if (pointer == 0) {
            pointer = 3;               // 3
        }    
        while (pointer < length) {
            regularPop = regularPop.substring(0, pointer) + "," + regularPop.substring( pointer, regularPop.length());
            length = regularPop.length();            // 10
            pointer += 1 + 3;
        }
        return regularPop;
    }
    // -------------------------------------------------// 
    /*
     *  return array of int [myPopulation][enemyPopulation]
     *  @param defCountry attackCountry
     *  @return int[]
     */
    public int[] defence(String defCountry, String attackCountry) {
        Random rand = new Random();
        int[] peopleList;
        peopleList = new int[3];
        Country ofMine = null;
        int mypop2 = 0;

        for (Country mine : this.countries) {
            if (mine.getName().equals(attackCountry)) {
                mypop2 = mine.getPopulation();           // population of my country
                ofMine = mine;
            } 
        }
        peopleList[0] = mypop2;

        for (Country aktualna : this.countries) {
            if (aktualna.getName().equals(defCountry)) {
                if (getAntiMiss(defCountry) == 0) {
                    System.out.println(">> Hit!");         // System.Out
                    peopleList = explode(defCountry, attackCountry);
                } else {
                    int all = rand.nextInt((10) + 1);
                    if (2 <= all && all <= 8) {
                        System.out.println(">> Failed! Anti-B hit Missile!");   // System.Out
                        setAntiMiss(-1, defCountry);
                        peopleList[1] = aktualna.getPopulation();
                    } else {
                        System.out.println(">> Hit! Anti-B missed!");
                        setAntiMiss(-1, defCountry);
                        peopleList = explode(defCountry, attackCountry);
                    }
                }
            }
        }
        return peopleList;
    }
    // -------------------------------------------------//
    /*
     *  if hit, make missile explode
     *  return [myPopulation][enemyPopulation]
     *  @param defCountry attackCountry
     *  @return int[]
     */
    public int[] explode(String defCountry, String attackCountry) {
        Random rand = new Random();
        int[] peopleList;
        peopleList = new int[3];
        Country ofMine = null;
        int mypop2 = 0;

        for (Country mine : this.countries) {
            if (mine.getName().equals(attackCountry)) {
                mypop2 = mine.getPopulation();           // population of my country
                ofMine = mine;
            } 
        }
        peopleList[0] = mypop2;

        for (Country aktualna : this.countries) {
            if (aktualna.getName().equals(defCountry)) {
                int all = rand.nextInt(10) + 1;
                double random = (aktualna.getPopulation() * 0.3) + ((aktualna.getPopulation() * 0.5) - (aktualna.getPopulation() * 0.3)) * rand.nextDouble();
                int alive = aktualna.getPopulation() - (int)random;
                aktualna.setPopulation(alive);
                peopleList[1] = aktualna.getPopulation(); // insert to list enemy new population
                System.out.println(">> " + String.format("%,d", (int)random) + " people of " + defCountry + " died!");         // System.Out
                if (aktualna.getPopulation() < 0) {
                    aktualna.setPopulation(0);
                    peopleList[1] = aktualna.getPopulation(); // insert to list enemy new population
                }

                if (3 <= all && all <= 5 && aktualna.getPopulation() < 850000) {
                    System.out.println(">> people of " + defCountry + " had joined to " + attackCountry);         // System.Out
                    int mypop = aktualna.getPopulation();
                    ofMine.setPopulation(mypop2 + mypop);    // set my population + enemy population
                    aktualna.setPopulation(0); 
                    peopleList[0] = ofMine.getPopulation(); // insert to list my new population
                    peopleList[1] = aktualna.getPopulation(); // insert to list enemy new population
                }

            }         
        }
        return peopleList;
    }
    // -------------------------------------------------//
    /*
     *  give population based on actual population
     *  @return void 
     */
    public void setPopulationByKoef() {
        int actPop = 0;
        int actBudg = 0;
        int randAddBudg = 0;
        double min = 0;
        double max = 0;
        double n = 0;
        for (Country aktualna : this.countries) {
            actPop = aktualna.getPopulation();
            if (actPop < 1000000) {
                max = actPop * 0.65;
                min = actPop * 0.35;
            } else if (1000000 <= actPop && actPop < 20000000) {
                max = actPop * 0.35;
                min = actPop * 0.1;
            } else {
                max = actPop * 0.18;
                min = actPop * 0.1;
            } 
            //n = rand.nextDouble(max) + min;
            //n = min + (n * (max - min));
            n = min + new Random().nextDouble() * (max - min);
            aktualna.setPopulation(actPop + (int)n);
            //----------------------------------------------------//
            actBudg = aktualna.getBudget();
            actPop = aktualna.getPopulation();
            if (actPop < 1000000) {
                n = actPop * 0.12;
            } else if (1000000 <= actPop && actPop < 20000000) {
                n = actPop * 0.035;
            } else {
                n = actPop * 0.015;
            } 
            aktualna.setBudget(actBudg + (int)n);

        }
    }
    // -------------------------------------------------// 
    /*
     *  return actual population
     *  @param country
     *  @return int 
     */
    public int getPopulation(String country) {
        int population = 0;
        for (Country aktualna : this.countries) {
            if (aktualna.getName().equals(country)) {
                population = aktualna.getPopulation();
            }         
        }
        return population;
    }
    // -------------------------------------------------//
    /*
     *  set population
     *  @param count country
     *  @return void 
     */
    public void setPopulation(int count, String country) {
        int population = 0;
        for (Country aktualna : this.countries) {
            if (aktualna.getName().equals(country)) {
                population = aktualna.getPopulation();
                aktualna.setPopulation(population + count);
            }         
        }
    }
    // -------------------------------------------------//
    /*
     *  return actaul quantity of missiles
     *  @param country
     *  @return int
     */
    public int getMiss(String country) {
        int missiles = 0;
        for (Country aktualna : this.countries) {
            if (aktualna.getName().equals(country)) {
                missiles = aktualna.getMissile();
            }         
        }
        return missiles;
    }
    // -------------------------------------------------//
    /*
     *  set missiles
     *  @param count country
     *  @return void 
     */
    public void setMiss(int count, String country) {
        int missiles = 0;
        for (Country aktualna : this.countries) {
            if (aktualna.getName().equals(country)) {
                missiles = aktualna.getMissile();
                aktualna.setMissile(missiles + count);
                //System.out.println(">> " + aktualna.getMissile());
            }         
        }
    }
    // -------------------------------------------------//
    /*
     *  return quantity of anti balistic missiles
     *  @param country
     *  @return int
     */
    public int getAntiMiss(String country) {
        int missiles = 0;
        for (Country aktualna : this.countries) {
            if (aktualna.getName().equals(country)) {
                missiles = aktualna.getAntiMissile();
                //System.out.println(">> " + aktualna.getAntiMissile());
            }         
        }
        return missiles;
    }
    // -------------------------------------------------// 
    /*
     *  set quantity of anti - b missiles
     *  @return void 
     */
    public void setAntiMiss(int count, String country) {
        int missiles = 0;
        for (Country aktualna : this.countries) {
            if (aktualna.getName().equals(country)) {
                missiles = aktualna.getAntiMissile();
                aktualna.setAntiMissile(missiles + count);
            }         
        }
    }
    // -------------------------------------------------// 
    /*
     *  change relationship choosen country with you
     *  @return void 
     */
    public void changeRelationShip() {
        for (Country aktualna : this.countries) {
            if (aktualna.getName().equals(this.nameOfChoosenCountry)) {
                if (!aktualna.getRelationshipWithYou().equals("At war!")) {
                    aktualna.setRelationshipWithYou("At war!");
                    System.out.println(">> " + this.nameOfChoosenCountry + " declares war at you!");
                }
            }         
        }
    }
    // -------------------------------------------------//
    /*
     *  return relationship 
     *  @param text
     *  @return string 
     */
    public String getRealtionship(String text) {
        String relat = "";

        for (Country aktualna : this.countries) {
            if (aktualna.getName().equals(text)) {
                relat = aktualna.getRelationshipWithYou();
            }         
        }
        return relat;
    }
    // -------------------------------------------------//
    /*
     *  return array of parameters like:
     *  budget, population, position, attack Missiles and deffence Missiles
     *  @param text
     *  @return int[]
     */
    public int[] getParameters(String text) {
        int[] myList;
        myList = new int[10];

        for (Country aktualna : this.countries) {
            if (aktualna.getName().equals(text)) {
                //System.out.println("Budget:     " + aktualna.getBudget());
                myList[0] = aktualna.getBudget();
                //System.out.println("Population: " + aktualna.getPopulation());
                myList[1] = aktualna.getPopulation();
                myList[2] = aktualna.getPosX();
                myList[3] = aktualna.getPosY();
                myList[4] = aktualna.getMissile();
                myList[5] = aktualna.getAntiMissile();
            }         
        }
        return myList;
    }
    // -------------------------------------------------//
    /*  Create coumtries with fixed atributtes
     *   add to contaner
     *  @return void 
     */
    public void createCountries() {

        this.algeria = new Country("Algeria", 170000, 41320000, 220, 320, 2, 3);
        this.countries.add(this.algeria);
        this.libya = new Country("Libya", 50980, 6375000, 400, 400, 1, 3);
        this.countries.add(this.libya);
        this.egypt = new Country("Egypt", 253000, 97550000, 539, 380, 2, 4);
        this.countries.add(this.egypt);
        this.saudiArabia = new Country("SaudiArabia", 638800, 32940000, 713, 434, 2, 5);
        this.countries.add(this.saudiArabia);
        this.iraq = new Country("Iraq", 197700, 38270000, 696, 313, 3, 5);
        this.countries.add(this.iraq);
        this.iran = new Country("Iran", 439500, 81160000, 824, 316, 4, 4);
        this.countries.add(this.iran);
        this.syria = new Country("Syria", 59150, 18270000, 613, 295, 1, 2);
        this.countries.add(this.syria);
        this.afghanistan = new Country("Afghanistan", 20820, 35530000, 963, 330, 3, 6);
        this.countries.add(this.afghanistan);
        this.turkmenistan = new Country("Turkmenistan", 42390, 5758000, 863, 220, 1, 3);
        this.countries.add(this.turkmenistan);
        this.uzbekistan = new Country("Uzbekistan", 48720, 32390000, 900, 177, 3, 3);
        this.countries.add(this.uzbekistan);
        this.kazakhstan = new Country("Kazakhstan", 159400, 18040000, 930, 59, 4, 5);
        this.countries.add(this.kazakhstan);
        this.turkey = new Country("Turkey", 851100, 79810000, 583, 228, 4, 7);
        this.countries.add(this.turkey);
        this.belarus = new Country("Belarus", 54440, 9508000, 473, 22, 2, 3);
        this.countries.add(this.belarus);
        this.ukraine = new Country("Ukraine", 112200, 44830000, 503, 71, 4, 6);
        this.countries.add(this.ukraine);
        this.romania = new Country("Romania", 211800, 19640000, 461, 136, 2, 3);
        this.countries.add(this.romania);
        this.bulgaria = new Country("Bulgaria", 56830, 7102000, 465, 183, 1, 2);
        this.countries.add(this.bulgaria);

        this.greece = new Country("Greece", 200300, 10770000, 431, 234, 3, 6);
        this.countries.add(this.greece);
        this.balkania = new Country("Balkania", 115000, 13895000, 402, 172, 4, 6);
        this.countries.add(this.balkania);
        this.hungary = new Country("Hungary", 139100, 9781000, 190, 123, 1, 2);
        this.countries.add(this.hungary);
        this.austria = new Country("Austria", 416600, 8773000, 326, 111, 3, 5);
        this.countries.add(this.austria);
        this.slovakia = new Country("Slovakia", 95770, 5435000, 395, 91, 1, 2);
        this.countries.add(this.slovakia);
        this.czechRep = new Country("CzechRepub", 215700, 10580000, 348, 79, 2, 4);
        this.countries.add(this.czechRep);
        this.poland = new Country("Poland", 524500, 39970000, 393, 46, 5, 6);
        this.countries.add(this.poland);
        this.germany = new Country("Germany", 3677000, 82790000, 285, 77, 8, 9);
        this.countries.add(this.germany);
        this.italy = new Country("Italy", 1935000, 60590000, 323, 192, 4, 6);
        this.countries.add(this.italy);
        this.france = new Country("France", 2583000, 67120000, 200, 153, 7, 10);
        this.countries.add(this.france);
        this.unitedKingdom = new Country("UnitedKingdom", 2622000, 66020000, 167, 42, 8, 9);
        this.countries.add(this.unitedKingdom);
        this.ireland = new Country("Ireland", 333700, 4784000, 92, 23, 1 , 2);
        this.countries.add(this.ireland);
        this.spain = new Country("Spain", 1311000, 46570000, 133, 244, 4, 6);
        this.countries.add(this.spain);
        this.portugal = new Country("Portugal", 217600, 10310000, 84, 207, 2, 3);
        this.countries.add(this.portugal);
        this.morocco = new Country("Morocco", 109100, 35740000, 94, 355, 1, 2);
        this.countries.add(this.morocco);
    }

}
