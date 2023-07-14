export default {
  template: "<div></div>",
  mounted() {
    this.map = L.map(this.$el);
    L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>',
    }).addTo(this.map);
    this.targets = [];
    this.markers = [];
  },
  methods: {
    set_location(latitude, longitude, label) {
      this.target = L.latLng(latitude, longitude);
      this.map.setView(this.target, 9);
      if (this.marker) {
        this.map.removeLayer(this.marker);
      }
      this.marker = L.marker(this.target).bindPopup(label);
      this.marker.addTo(this.map);
    },
    set_multi_locations(locations) {
      // Remove all markers from the map
      for (let marker of this.markers) {
        this.map.removeLayer(marker);
        console.log(marker)
      }
      this.markers = [];
      // add points to map (markers)
      for (let location of locations) {
        this.targets.push(location);
        const [latitude, longitude, label] = location;
        //console.log(latitude, longitude, label);
        const target = L.latLng(latitude, longitude);
        this.map.setView(target, 12);
        const marker = L.marker(target).bindPopup(label).addTo(this.map);     //add markers to list
        //.on('click', function(e) {console.log(e.label);
        this.markers.push(marker);   
      }
    },
//
    clear_map() {
      // Remove all markers from the map
      for (let marker of this.markers) {
        this.map.removeLayer(marker);
        //console.log(marker)
      }
      this.markers = [];

    },//
  },
};
