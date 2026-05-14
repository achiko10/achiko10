# პრემიუმ უძრავი ქონების პლატფორმის ტექნიკური გეგმა

## 1. ტექნოლოგიური სტეკი
*   **ბექენდი (Core Logic):** Django (Python). გამოიყენება მონაცემთა ბაზის სამართავად, რთული ფილტრაციის ლოგიკისთვის (ფასი, კვადრატულობა, სართული, ოთახების რაოდენობა) და შიდა CRM სისტემასთან (გაყიდვების მენეჯერებისთვის) სინქრონიზაციისთვის.
*   **რეალურ დროში განახლებები:** Firebase Realtime Database. უზრუნველყოფს ჯავშნების მომენტალურ ასახვას. თუ ერთი მომხმარებელი დაჯავშნის ბინას, სხვა მომხმარებლებთან სტატუსი ("თავისუფალია" -> "დაჯავშნილია") წამიერად შეიცვლება გვერდის დარეფრეშების გარეშე.
*   **ფრონტენდი:** Pure HTML/CSS/JS "Crystal Bricks" დიზაინის ლოგიკისთვის.

## 2. მონაცემთა ბაზის მოდელები (Django ORM)

```python
class Project(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    completion_date = models.DateField()

class Apartment(models.Model):
    STATUS_CHOICES = (
        ('available', 'თავისუფალია'),
        ('reserved', 'დაჯავშნილია'),
        ('sold', 'გაყიდულია'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    block = models.CharField(max_length=10)
    floor = models.IntegerField()
    door_number = models.CharField(max_length=10)
    area_sqm = models.DecimalField(max_digits=6, decimal_places=2) # კვადრატულობა
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # 3D მოდელისა და გალერეის ბმულები
    virtual_tour_url = models.URLField(blank=True, null=True)
    isometric_image = models.ImageField(upload_to='apartments/isometric/')
```

## 3. 3D და გალერეის ინტეგრაციის ლოგიკა (Frontend)
*   **Isometric View (იზომეტრიული ხედი):** მთავარ გვერდზე შენობის მოდელი წარმოდგენილია ინტერაქტიული SVG ან Canvas ობიექტის სახით. თითოეული სართული/ბინა არის ცალკეული clickable ფენა (layer).
*   **WebGL / Three.js:** თუ მოთხოვნილია სრული 3D ნავიგაცია, გამოიყენება Three.js შენობის კრისტალური მოდელის სარენდეროდ.
*   **UI სინქრონიზაცია:** როდესაც მომხმარებელი ატარებს მაუსს (hover) ბინის 3D ბლოკზე, JavaScript უკავშირდება ბექენდს (ან კითხულობს წინასწარ ჩატვირთულ JSON-ს) და ეკრანზე გამოაქვს მქრქალი შუშის (Frosted Glass) საინფორმაციო ბარათი ფასითა და კვადრატულობით.
*   **Firebase Listener:** ბინის შეძენის/დაჯავშნის ღილაკზე დაჭერისას, `Firebase.database().ref('apartments/' + id).update({status: 'reserved'})` ირთვება, რაც ავტომატურად უცვლის ფერს ამ 3D ბლოკს ყველა სხვა მომხმარებლის ეკრანზე (მაგ: მწვანიდან წითლად).
